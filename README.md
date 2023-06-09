# dudaji-chat-exam

- 현재 아주 간단하게 동작하는 chatting 코드가 있습니다.
- 해당 코드는 동작하지만 개선해야할 부분이 많이 있습니다.
- 아래 이슈를 해결 부탁드립니다.
# 해결한 이슈
- [X] requirements.txt를 통해서 package가 관리되게 해주세요.
- [X] .gitignore를 등록해주세요.
- [X] lint를 적용해주세요.
- [X] print를 logging library로 변경해주시고, 좋은 포멧터를 적용한 뒤, 파일에도 로그가 남게 해주세요.
- [X] packet protocol을 json 혹은 protobuf로 변경해주세요.
- [X] recv / send를 포함하여 리팩토링을 진행하고, 불안정한 코드를 튼튼하게 수정해주세요. (hint: command pattern 적용 등)
- [X] 각종 매직넘버를 config를 통해서 관리하도록 해주세요.
- [X] README.md파일에 Quick start 문서를 작성해주세요.
# Quick Start
### 환경 설정
- 먼저 repository를 clone합니다.
```Text
git clone https://github.com/twotwobread/dudaji-chat-exam.git [DIR]
```
- 이후 clone한 프로젝트 루트 디렉토리(.git 파일이 존재하는 경로)에서 아래와 같은 명령어를 칩니다.
```
git install -r requirements.txt
pre-commit install
```
### 프로그램 구동
- server 프로그램을 구동하기 위해서 `app.py`를 실행합니다.
```
// 프로젝트 루트 디렉토리 상에서 `app.py` 실행
./app/app.py
```
- 이후 다른 프로세스를 이용해서 client.py를 여러 개 실행합니다.
```
// 프로젝트 루트 디렉토리 상에서 `app.py` 실행
./client.py
```
### 기능 설명
- client 측에서 메시지를 보내면 server에 접속한 모든 client들에게 메시지가 전송됩니다.
- client는 `quit`이라는 메시지를 보내서 프로그램을 종료할 수 있습니다.
### 부가 설명
- lint는 pre-commit을 활용하여 commit이 될 때 자동으로 적용되도록 설정했습니다.
