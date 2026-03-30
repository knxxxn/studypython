from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import time
import random
from datetime import datetime
from zoneinfo import ZoneInfo
from macro_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG
SEOUL_TZ = ZoneInfo("Asia/Seoul")


# ─────────────────────────────
# 정밀 타이밍 대기
# ─────────────────────────────
def precise_wait(target_time):
    while True:
        now = datetime.now(SEOUL_TZ)
        diff = (target_time - now).total_seconds()

        if diff <= 0.2:
            break

        time.sleep(0.01)


# ─────────────────────────────
# 메인 실행
# ─────────────────────────────
with Stealth().use_sync(sync_playwright()) as p:
    browser = p.chromium.launch(
        headless=False,
        args=[
            "--window-size=1600,900",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ],
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        locale="ko-KR",
        viewport={"width": 1600, "height": 900},
    )

    page = context.new_page()

    try:
        # ───────── 로그인
        page.goto("https://www.yes24.com/Templates/FTLogin.aspx")

        page.mouse.move(random.randint(200, 400), random.randint(200, 400))
        time.sleep(random.uniform(0.1, 0.3))
        page.mouse.move(random.randint(500, 700), random.randint(300, 500))
        time.sleep(random.uniform(0.1, 0.3))

        page.click('#SMemberID')
        page.keyboard.type(config.user_id, delay=random.randint(30, 80))

        time.sleep(random.uniform(0.2, 0.5))
        page.click('#SMemberPassword')
        page.keyboard.type(config.user_pw, delay=random.randint(30, 80))

        time.sleep(random.uniform(0.3, 0.7))
        page.click('#btnLogin')

        page.wait_for_load_state('domcontentloaded')
        time.sleep(random.uniform(1.0, 2.0))

        # ───────── 메인 페이지 경유
        page.goto("https://www.yes24.com")
        time.sleep(random.uniform(1.0, 2.0))

        # ───────── 이벤트 페이지
        page.goto(config.event_url)

        if not config.dry_run:
            print("⏳ 오픈 대기 중...")
            precise_wait(config.open_time)

        # ───────── 예매 클릭
        time.sleep(1)
        page.evaluate("jsf_pdi_GoPerfSale(77)")
        print("🎫 예매 버튼 클릭 완료")

        # ───────── 팝업 감지
        ticket_page = context.wait_for_event("page", timeout=30000)
        ticket_page.wait_for_load_state("domcontentloaded")
        print("🎯 팝업 진입 성공!")

        # ───────── step1: 날짜 클릭
        time.sleep(1)
        ticket_page.locator(f'a[id="{config.perf_date}"]').click()
        print(f"📅 날짜 선택: {config.perf_date}")

        # ───────── step1: 회차 선택 (JS 변수 직접 설정)
        ticket_page.wait_for_selector('#ulTime li', timeout=10000)
        time.sleep(0.5)

        # 회차 선택 + 조건 설정 + fdc_FlashSeatLoad 직접 호출 (한 번에)
        result = ticket_page.evaluate(f'''() => {{
            var li = document.querySelectorAll('#ulTime li')[{config.perf_time_index}];
            if (!li) return "NO_LI";

            // li에 on 클래스 추가
            $j('#ulTime li').removeClass('on');
            $j(li).addClass('on');

            // 필요한 값 모두 설정
            var idTime = li.getAttribute("value");
            $j("#IdTime").val(idTime);
            jgIdSelTime = idTime;

            // 조건 확인
            var chk1 = $j("#IdTime").val();
            var chk2 = $j("#ulTime > li.on").length;
            if (!chk1 || chk1 == "0" || chk2 == 0) {{
                return "FAIL: IdTime=" + chk1 + ", li.on=" + chk2;
            }}

            // 바로 좌석 로딩 호출 (fdc_ChoiceSeat 내부의 핵심 함수)
            fdc_FlashSeatLoad();
            return "OK: idTime=" + idTime;
        }}''')
        print(f"🪑 좌석선택 진입: {result}")

        # iframe이 실제로 로딩될 때까지 반복 시도
        seat_frame = None
        for attempt in range(5):
            # 1) iframe src가 DOM에 설정됐는지 확인
            for _ in range(10):
                time.sleep(0.5)
                src = ticket_page.evaluate('''() => {
                    var f = document.querySelector('iframe[name="ifrmSeatFrame"]');
                    return f ? f.src : "";
                }''')
                if 'PerfSaleHtmlSeat' in src:
                    break
            else:
                # src가 안 잡히면 fdc_FlashSeatLoad 재호출
                print(f"  ⏳ iframe src 미설정, 재시도 ({attempt + 2})...")
                ticket_page.evaluate('fdc_FlashSeatLoad()')
                continue

            # 2) Playwright 프레임 등록 대기
            for _ in range(20):
                time.sleep(0.5)
                for f in ticket_page.frames:
                    if 'PerfSaleHtmlSeat' in f.url:
                        seat_frame = f
                        break
                if seat_frame:
                    break

            if seat_frame:
                break
            print(f"  ⏳ 프레임 등록 대기 실패, 재시도 ({attempt + 2})...")
            ticket_page.evaluate('fdc_FlashSeatLoad()')

        if not seat_frame:
            print("❌ 좌석 iframe을 찾지 못함")
            input("종료하려면 Enter")
            raise SystemExit

        print("🖼️ 좌석 iframe 진입!")

        # 좌석 로딩 대기 → Playwright 네이티브 클릭으로 선택
        seat_frame.wait_for_selector('div[name="tk"]', timeout=15000)
        time.sleep(1)

        # 보이는 좌석 중 첫 번째를 Playwright 클릭 (실제 마우스 이벤트)
        seats = seat_frame.locator('div[name="tk"]')
        count = seats.count()
        selected = 0
        for i in range(count):
            seat = seats.nth(i)
            if seat.is_visible():
                seat.click()
                selected += 1
                time.sleep(0.3)
                if selected >= 1:
                    break
        print(f"🪑 좌석 {selected}석 선택!")
        time.sleep(1)

        # 좌석선택 완료 버튼 클릭 (Playwright 네이티브 클릭)
        seat_frame.locator('a:has(img.booking)').click()
        print("✅ 좌석선택 완료 클릭! 서버 확인 대기...")

        for i in range(60):
            time.sleep(0.5)
            area_display = ticket_page.evaluate(
                'document.getElementById("SeatFlashArea").style.display'
            )
            if area_display == 'none':
                break
            if i % 10 == 9:
                print(f"  ⏳ 서버 응답 대기 중... ({(i+1)*0.5:.0f}초)")
        else:
            print("⚠️ SeatFlashArea가 안 닫힘 — 수동으로 좌석선택 완료 눌러주세요")
            input("완료 후 Enter...")

        print("➡️ 좌석 확정 완료, 다음단계 이동")
        time.sleep(1)

        # ───────── step2 → step3: 다음단계
        ticket_page.evaluate('fdc_VerifySelSeatNumber()')
        time.sleep(2)

        # ───────── step3: 할인/쿠폰 단계
        ticket_page.wait_for_selector('#StepCtrlBtn03', state='visible', timeout=30000)
        print("🎫 할인/쿠폰 단계 도착! 여기서부터 수동으로 진행하세요.")
        input("결제까지 완료하면 Enter...")

        # ───────── step5: 결제
        ticket_page.click(config.payment_xpath)
        ticket_page.select_option('#selBank', index=config.bank_select_index)
        ticket_page.click('#cbxAllAgree')

        if not config.dry_run:
            ticket_page.click('#imgPayEnd')
            print("🎉 결제 완료!")
        else:
            print("🧪 dry_run 모드 — 결제 버튼 안 누름")

        input("종료하려면 Enter")

    finally:
        browser.close()
