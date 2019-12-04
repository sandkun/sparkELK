# python Selenium을 이용한 유튜브 데이터 수집
유튜브 채널의 정보를 elasticsearch에 저장하는 크롤러입니다.

# 주요기능
<img width="193" alt="스크린샷 2019-12-04 오후 4 21 42" src="https://user-images.githubusercontent.com/34993466/70121890-dadb0d00-16b2-11ea-9cc9-0519c2a725b9.png"> <br>
채널 ID를 입력하면 해당 채널의 정보를 **6시간** 마다 elasticsearch에 저장합니다.
<br>
저장되는 정보로는
**채널ID, 채널이름, 구독자수, 수집일시, 업로드 영상 (url, 조회수)**
```
{
  "id" : "채널 ID",
  "name" : "채널 이름",
  "subscriber" : "구독자 수",
  "date" : "수집일시" //format -> 2019-12-04 15:15:53
  "videos" : [
    {
      url : "영상 url",
      view : "해당 영상 조회수"
    },
    ...
  ]
}
```
추가적인 정보들은 elasticsearch의 집계합수를 이용하여 정보를 집계할 수 있음 <br>
EX) 총 조회수

# Todo
크롤링한 데이터를 바탕으로 유튜브 채널의 프로필을 제작하는 것을 해보고 싶다.
