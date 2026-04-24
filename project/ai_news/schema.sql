-- ⚠️ 기존 schema.sql(auth.sql)의 테이블이 이미 만들어져 있다면, 
-- 먼저 기존 테이블을 삭제하고 이 스크립트를 실행해주세요.

-- 기존 테이블 삭제 (이미 있는 경우)
DROP TABLE IF EXISTS public.calendars;
DROP TABLE IF EXISTS public.memos;
DROP TABLE IF EXISTS public.todos;

-- 1. Todos 테이블 (날짜별 투두 목록을 JSON 배열로 저장)
CREATE TABLE public.todos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    date TEXT NOT NULL,                    -- "2026-04-24" 형식
    items JSONB NOT NULL DEFAULT '[]',     -- [{"text":"할일","done":false}, ...]
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(user_id, date)                  -- 같은 유저, 같은 날짜에 중복 방지
);

-- 2. Memos 테이블 (날짜별 메모 텍스트 저장)
CREATE TABLE public.memos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    date TEXT NOT NULL,                    -- "2026-04-24" 형식
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(user_id, date)
);

-- 3. Calendars (D-Day) 테이블
CREATE TABLE public.calendars (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- RLS (Row Level Security) 활성화
ALTER TABLE public.todos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.memos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.calendars ENABLE ROW LEVEL SECURITY;

-- 정책: 본인 데이터만 접근 가능
CREATE POLICY "Users can view own todos" ON public.todos FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own todos" ON public.todos FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own todos" ON public.todos FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own todos" ON public.todos FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own memos" ON public.memos FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own memos" ON public.memos FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own memos" ON public.memos FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own memos" ON public.memos FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own calendars" ON public.calendars FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own calendars" ON public.calendars FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own calendars" ON public.calendars FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own calendars" ON public.calendars FOR DELETE USING (auth.uid() = user_id);
