
# KSC 웹사이트 프로젝트

## 프로젝트 개요
이 프로젝트는 Flask 프레임워크를 기반으로 한 웹 애플리케이션으로, 경설컴(KSC) 동아리의 회원 관리 및 게시판 기능을 제공합니다. 사용자는 회원가입과 로그인, 게시물 작성 및 삭제 등의 기능을 이용할 수 있습니다.

## 주요 기능
1. **회원가입 및 로그인**
   - 사용자 정보를 입력하여 새로운 계정을 생성하고, 로그인한 사용자만이 접근할 수 있는 기능을 제공합니다.
   - Flask Session을 이용하여 로그인 상태를 유지하며, 로그인된 사용자 정보는 세션 쿠키에 암호화되어 저장됩니다.

2. **공지사항**
   - 로그인한 사용자만이 공지사항 글을 작성, 수정, 삭제할 수 있습니다.
   - 로그인과 무관하게 작성된 글을 검색, 확인할 수 있습니다.

3. **게시판 기능**
   - 사용자들이 질문이나 게시물을 작성하고, 수정 및 삭제할 수 있습니다.
   - 게시물 정보는 SQLite 데이터베이스에 저장되며, ORM 라이브러리인 SQLAlchemy를 통해 데이터베이스와 상호작용합니다.

3. **관리자 페이지**
   - 접근 방법: `KSC_Web_DB_Control_2.py`에서 추가 url인 `/admin`을 작성하면 관리자 페이지로 접속됩니다.
   - 관리자는 모든 사용자 정보를 조회하고 관리할 수 있습니다.
   - 특정 사용자의 정보 수정 및 삭제가 가능하며, 권한에 따른 접근 제어가 이루어집니다.
   - ![img.png](img.png)

## 사용된 기술 스택
- **프레임워크**: Flask
- **데이터베이스**: SQLite
- **ORM**: SQLAlchemy
- **프론트엔드**: HTML, CSS, JavaScript
- **세션 관리**: Flask Session

## 설치 및 실행 방법
1. **필요한 패키지 설치**
   ```
   pip install flask flask_sqlalchemy
   ```
2. **애플리케이션 실행**
   ```
   python KSC_Web.py
   ```
3. **웹사이트 접속**
   로컬 서버 `http://127.0.0.1:5000`에 접속하여 기능을 테스트합니다.

## 프로젝트 폴더 구조
```
FlaskApp_6
├── DataBase                  # SQLite 데이터베이스
├── KSC_Web.py                # 메인 애플리케이션 파일
├── KSC_Web_Box.py
├── KSC_Web_DB_Control.py
├── KSC_Web_DB_Control_2.py
├── KSC_Web_Introduce.py
├── KSC_Web_Main_New.py
├── KSC_Web_MyPage.py
├── KSC_Web_Notice.py
├── KSC_Web_Post.py
├── KSC_Web_Sign_InUp.py
├── instance
├── migrations
├── static                    # 정적 파일 (CSS, JavaScript, 이미지 등)
└── templates                 # HTML 템플릿 파일
```



## 데이터베이스 모델 구조
1. **User 테이블**
   - id: 정수형, 기본키
   - username: 문자열(100), 유니크, 필수
   - password: 문자열(100), 필수
   - email: 문자열(120), 유니크, 필수
   - birth_date: 문자열(10), 필수
   - first_name: 문자열(50), 필수
   - last_name: 문자열(50), 필수

2. **Question 테이블**
   - id: 정수형, 기본키
   - title: 문자열(200), 필수
   - content: 텍스트, 필수
   - user_id: 정수형, 외래키(User.id)

3. **Answer 테이블**
   - id: 정수형, 기본키
   - question_id: 정수형, 외래키(Question.id)
   - content: 텍스트, 필수
   - user_id: 정수형, 외래키(User.id)
   - timestamp: 문자열(50), 필수

4. **Comment 테이블**
   - id: 정수형, 기본키
   - answer_id: 정수형, 외래키(Answer.id)
   - content: 텍스트, 필수
   - user_id: 정수형, 외래키(User.id)
   - timestamp: 문자열(50), 필수

## 각 페이지 설명
1. **홈페이지** (`/`): 프로젝트의 메인 페이지로, 주요 기능 및 설명을 제공합니다.
2. **회원가입 페이지** (`/register`): 사용자가 회원가입을 할 수 있는 페이지입니다.
3. **로그인 페이지** (`/login`): 사용자가 로그인할 수 있는 페이지입니다.
4. **게시판 목록 페이지** (`/questions`): 게시판의 모든 질문 목록을 확인할 수 있습니다.
5. **질문 작성 페이지** (`/questions/new`): 새로운 질문을 작성할 수 있는 페이지입니다.
6. **질문 상세 페이지** (`/questions/<question_id>`): 특정 질문의 상세 내용을 보고, 답변을 추가할 수 있습니다.
7. **마이페이지** (`/mypage`): 로그인한 사용자가 자신의 정보를 확인하고 수정할 수 있는 페이지입니다.
8. **관리자 페이지** (`/admin`): 관리자가 사용자 정보를 관리할 수 있는 페이지입니다.(추가 예정)


## 기여 방법
- 이 프로젝트에 기여하고 싶다면, 먼저 새로운 브랜치를 만들어 변경 사항을 커밋하고 Pull Request를 제출해 주세요.

## 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자유롭게 수정 및 사용하되, 라이선스를 명시해 주세요.
