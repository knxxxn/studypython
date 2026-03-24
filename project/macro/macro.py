from playwright.sync_api import sync_playwright
import time
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
# 좌석 자동 선택 스크립트
# ─────────────────────────────
SEAT_SCRIPT = """
(() => {
    if (window.__seat_auto) return;
    window.__seat_auto = true;

    function clickConfirm() {
        // 더 넓은 범위로 확인 버튼 탐색
        let selectors = [
            '#btnSeatOk',
            'a[onclick*="SeatOk"]',
            'img[src*="btn_seat_ok"]',
            'a[onclick*="seatOk"]',
            'input[type=button][value*="선택완료"]',
            'a[href*="SeatOk"]'
        ];
        for (let sel of selectors) {
            let btn = document.querySelector(sel);
            if (btn) {
                console.log('[AUTO] 확인 버튼 클릭:', sel);
                btn.click();
                return true;
            }
        }
        console.warn('[AUTO] 확인 버튼 못 찾음');
        return false;
    }

    function pickSeat() {
        let seats = document.querySelectorAll('img[src*="seat"], div[title]');
        for (let seat of seats) {
            let rect = seat.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                seat.click();
                console.log('[AUTO] 좌석 클릭:', seat);
                // 클릭 직후 확인 버튼도 바로 대기
                setTimeout(() => {
                    let tries = 0;
                    let t = setInterval(() => {
                        if (clickConfirm() || tries++ > 30) clearInterval(t);
                    }, 100);
                }, 150);
                return true;
            }
        }
        return false;
    }

    let tries = 0;
    let interval = setInterval(() => {
        if (pickSeat() || tries++ > 100) clearInterval(interval);
    }, 30);
})();
"""


def inject_script(frame):
    try:
        frame.evaluate(SEAT_SCRIPT)
    except:
        pass


# ─────────────────────────────
# 메인 실행
# ─────────────────────────────
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=[
            "--window-size=1600,900",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ],
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        locale="ko-KR",
        viewport={"width": 1600, "height": 900},
    )

    # 🔥 초강력 Stealth 설정 (STClab 봇 탐지 우회)
    stealth_js = """
        // 1. webdriver 플래그 완벽 제거
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
        
        // 2. Chrome 속성 위장
        window.chrome = {
            runtime: {},
            app: {},
            csi: () => {},
            loadTimes: () => {}
        };
        
        // 3. 권한 상태 조작 (알림 등)
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => {
            return parameters.name === 'notifications' 
                ? Promise.resolve({ state: Notification.permission }) 
                : originalQuery(parameters);
        };
        
        // 4. 플러그인 및 언어 조작
        Object.defineProperty(navigator, 'languages', { get: () => ['ko-KR', 'ko', 'en-US', 'en'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        
        // 5. User-Agent에서 Headless 흔적이나 비정상 흔적 제거
        Object.defineProperty(navigator, 'userAgent', {
            get: () => "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        });
        
        // 6. 하드웨어 정보 속이기 (Concurrency, Memory)
        Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
        Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
        
        // 7. WebGL 벤더 속이기
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) return 'Intel Inc.'; // UNMASKED_VENDOR_WEBGL
            if (parameter === 37446) return 'Intel Iris OpenGL Engine'; // UNMASKED_RENDERER_WEBGL
            return getParameter.apply(this, [parameter]);
        };
    """
    context.add_init_script(stealth_js)

    page = context.new_page()

    try:
        # ───────── 로그인 (사람처럼)
        page.goto("https://www.yes24.com/Templates/FTLogin.aspx")

        page.mouse.move(300, 300)
        page.mouse.move(600, 400)

        page.click('#SMemberID')
        page.keyboard.type(config.user_id, delay=50)

        page.click('#SMemberPassword')
        page.keyboard.type(config.user_pw, delay=50)

        time.sleep(0.3)
        page.click('#btnLogin')

        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)

        # ───────── 이벤트 페이지
        page.goto(config.event_url)

        print("⏳ 오픈 대기 중...")
        precise_wait(config.open_time)

        # ───────── 예매 클릭   
        btn = page.locator('a:has(img[src*="btn_reserve"]), a.btn_reserve').first
        btn.scroll_into_view_if_needed()
        time.sleep(0.1)
        btn.click()
        
        # 사용자가 아무 때나 클릭해서 새 창(팝업)이 열리면 그걸 낚아챔
        ticket_page = context.wait_for_event("page", timeout=0)
        ticket_page.wait_for_load_state("domcontentloaded")
        print("🎯 팝업(좌석/날짜 선택창) 진입 감지 성공!")

        # ───────── 좌석 스크립트 주입 (팝업 창과 거기서 열리는 프레임 모두)
        ticket_page.add_init_script(SEAT_SCRIPT)
        ticket_page.on("frameattached", lambda f: inject_script(f))

        print("🪑 좌석 자동 선택 대기")

        # ✅ 이 부분 추가 - 좌석 선택 화면 HTML 덤프
        time.sleep(2)  # 페이지 로딩 대기
        html = ticket_page.content()
        with open("dump.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("📄 dump.html 저장 완료 - VS Code에서 열어서 버튼 확인하세요")

        # ───────── 결제 단계
        ticket_page.wait_for_selector('//*[@id="StepCtrlBtn03"]/a[2]/img', timeout=600000)

        print("💳 결제 단계 진입")

        ticket_page.click('//*[@id="StepCtrlBtn03"]/a[2]/img')
        time.sleep(0.3)

        ticket_page.click('//*[@id="StepCtrlBtn04"]/a[2]/img')
        time.sleep(0.3)

        ticket_page.click(config.payment_xpath)
        ticket_page.select_option('#selBank', index=config.bank_select_index)

        ticket_page.click('#cbxAllAgree')

        if not config.dry_run:
            ticket_page.click('#imgPayEnd')
            print("🎉 결제 완료")

        input("종료하려면 Enter")

    finally:
        browser.close()