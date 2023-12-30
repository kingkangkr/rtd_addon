
import tkinter as tk

class UnitTrackerApp:
    def __init__(self, frame, quest_name, unit_names, column_titles):
        self.frame = frame
        self.unit_counts = {name: tk.IntVar(value=0) for name in unit_names}

        # 퀘스트 이름 레이블 생성 및 표시
        quest_name_label = tk.Label(self.frame, text=quest_name)
        quest_name_label.grid(row=0, column=0, columnspan=5)

        # 각 열의 제목 설정
        for col, title in enumerate(column_titles):
            tk.Label(self.frame, text=title).grid(row=1, column=col)

            # 5x8 행렬 레이아웃 및 각 열별 초기화 버튼 생성
            for i, name in enumerate(unit_names, 1):
                row = (i - 1) % 8 + 2  # 제목 행을 고려하여 +2
                column = (i - 1) // 8

                unit_frame = tk.Frame(self.frame)
                unit_frame.grid(row=row, column=column)

                tk.Label(unit_frame, text=name).grid(row=0, column=0, columnspan=3)
                tk.Label(unit_frame, textvariable=self.unit_counts[name]).grid(row=1, column=0)
                tk.Button(unit_frame, text="+", command=lambda name=name: self.increment_count(name)).grid(row=1, column=2)
                tk.Button(unit_frame, text="-", command=lambda name=name: self.decrement_count(name)).grid(row=1, column=1)
                # 마지막 행에 열별 초기화 버튼 추가
                for col, title in enumerate(column_titles):
                    reset_button = tk.Button(self.frame, text=f"{title} 초기화",
                                             command=lambda c=col: self.reset_column(c))
                    reset_button.grid(row=11, column=col)  # 모든 유닛 프레임 아래에 위치

    def increment_count(self, name):
        self.unit_counts[name].set(self.unit_counts[name].get() + 1)

    def decrement_count(self, name):
        if self.unit_counts[name].get() > 0:
            self.unit_counts[name].set(self.unit_counts[name].get() - 1)

    def reset_column(self, column):
        for i, name in enumerate(self.unit_counts, 1):
            if (i - 1) // 8 == column:
                self.unit_counts[name].set(0)

# 전체 초기화 함수
def reset_all(app):
    for name in app.unit_counts:
        app.unit_counts[name].set(0)
def switch_frame(frame_to_raise):
    frame_to_raise.tkraise()
# 메인 함수
mission_requirements = {
    "기본 편식": {"마린": 1, "벌처": 1, "레이스": 1,"히드라": 1, "뮤탈": 1, "울트라": 1, "드라군": 1, "스카웃": 1},
    "노랑 편식": {"노랑 파뱃": 1, "노랑 탱크": 1, "노랑 남고": 1,"노랑 여고": 1, "노랑 디파": 1, "노랑 아칸": 1, "노랑 닼템": 1, "노랑 스카웃": 1},
    "그남그여": {"노랑 여고": 1, "노랑 남고": 1},
    "쩜드라": {"유니크 히드라" : 3},
    "스타쉽 트루퍼스": {"유니크 발키리": 1, "유니크 가디언": 1, "파랑 디바": 1, "파랑 파뱃": 1, "노랑 탱크" : 1, "노랑 디파" : 1, "뮤탈": 1, "벌처": 1},
    "인디펜던스 데이": {"유니크 발키리": 1, "유니크 리버": 1, "파랑 드라군": 1, "파랑 파뱃": 1, "노랑 탱크" : 1, "노랑 아칸" : 1, "드라군": 1, "벌처": 1},
    "이취": {"유니크 마린": 1, "유니크 저글링": 1,"유니크 가디언": 1, "유니크 아칸": 1, "유니크 하템": 1, "유니크 히드라": 1, "유니크 발키리": 1},
    "더키헬": {"에픽 럴커" : 3},
    "탄핵": {"에픽 하템": 2, "에픽 케리건": 1},
    "디9": {"파랑 아비터": 3, "파랑 남고": 3, "노랑 아칸" : 3, "노랑 여고": 3},
    "나빼고": {"유니크 마린": 2, "유니크 아칸": 2, "파랑 레이스": 2, "파랑 아비터": 2, "노랑 스카웃": 2, "노랑 파뱃": 2},
    "자리미션": {"노랑 디파": 7, "노랑 닼템": 7}
}

def create_mission_status_frame(frame, unit_tracker_app, mission_status_label):
    update_mission_status(mission_requirements, unit_tracker_app, mission_status_label)

def update_mission_status(mission_requirements, unit_tracker_app, mission_status_label):
    status_text = calculate_mission_status(mission_requirements, unit_tracker_app)
    mission_status_label.config(text=status_text)

def calculate_mission_status(mission_requirements, unit_tracker_app):
    status_text = ""
    for mission, requirements in mission_requirements.items():
        status_text += f"{mission}:\n"
        for unit, required_count in requirements.items():
            current_count = unit_tracker_app.unit_counts[unit].get()
            if current_count < required_count:
                status_text += f"{unit} {required_count - current_count}개 부족합니다.\n"
            else:
                status_text += f"{unit} 충족됨.\n"
    return status_text
def create_scrollable_frame(root):
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 스크롤 휠 이벤트 처리 추가
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame

def main():
    root = tk.Tk()
    root.title("랜타디 트래커")
    frame1 = tk.Frame(root)
    frame2 = tk.Frame(root)

    for frame in (frame1, frame2):
        frame.grid(row=0, column=0, sticky='nsew')

    unit_names = ["마린", "벌처", "레이스", "히드라", "뮤탈", "울트라", "드라군", "스카웃", "노랑 파뱃", "노랑 탱크", "노랑 남고", "노랑 여고", "노랑 디파",
                  "노랑 아칸", "노랑 닼템", "노랑 스카웃", "파랑 디바", "파랑 디파", "파랑 골리앗", "파랑 아비터", "파랑 레이스", "파랑 파뱃", "파랑 남고",
                  "파랑 드라군", "유니크 가디언", "유니크 저글링", "유니크 히드라", "유니크 아칸", "유니크 마린", "유니크 발키리", "유니크 하템", "유니크 리버", "에픽 럴커",
                  "에픽 고스트", "에픽 케리건", "에픽 하템", "에픽 벌처", "에픽 캐리어", "에픽 뮤탈", "에픽 야마토"]
    column_titles = ["노멀", "노랑(매직)", "파랑(레어)", "유니크", "에픽"]  # 각 열의 제목

    app1 = UnitTrackerApp(frame1, "랜타디", unit_names, column_titles)
    frame2_scrollable = create_scrollable_frame(frame2)
    # 페이지 2 미션 상태 레이블
    mission_status_label = tk.Label(frame2)
    mission_status_label.pack()
    mission_status_label = tk.Label(frame2_scrollable)
    mission_status_label.pack()
    # 페이지 2 미션 상태 생성 및 추적
    create_mission_status_frame(frame2, app1, mission_status_label)

    # 유닛 수 변경 시 미션 상태 업데이트
    for var in app1.unit_counts.values():
        var.trace_add("write", lambda *args: update_mission_status(mission_requirements, app1, mission_status_label))
    current_page = [frame1]

    def toggle_page(event):
        if current_page[0] == frame1:
            switch_frame(frame2)
            current_page[0] = frame2
        else:
            switch_frame(frame1)
            current_page[0] = frame1

    root.bind('<Tab>', toggle_page)

    # 페이지 전환 버튼
    btn_page1 = tk.Button(root, text="페이지 1", command=lambda: switch_frame(frame1))
    btn_page2 = tk.Button(root, text="페이지 2", command=lambda: switch_frame(frame2))

    btn_page1.grid(row=1, column=0)
    btn_page2.grid(row=1, column=1)

    switch_frame(frame1)

    root.mainloop()


if __name__ == "__main__":
    main()


