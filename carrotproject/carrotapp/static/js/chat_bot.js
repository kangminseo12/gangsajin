document.getElementById('sendButton').addEventListener('click', function () {
    // 로딩 애니메이션 
    // document.getElementById('loading-animation').style.display = 'block';
    // document.getElementById('ai-img').style.display = 'none';
    let currentDate = new Date();

    // 한국 시간대 (KST, Asia/Seoul)로 설정합니다.
    const monthNames = [
        '1월', '2월', '3월', '4월', '5월', '6월',
        '7월', '8월', '9월', '10월', '11월', '12월'
      ];
    const addLeadingZero = (number) => {
        if (number < 10) {
            return `0${number}`;
        }
        return number;
        };
    
    // 날짜와 시간을 원하는 형식으로 포맷합니다.
    let koreaTime = `${currentDate.getFullYear()}년 ${monthNames[currentDate.getMonth()]} ${currentDate.getDate()}일 ${currentDate.getHours()}:${addLeadingZero(currentDate.getMinutes())}`;
    

    let title = document.getElementById('message-textarea').value;

    let msg_you = document.querySelector(".chat-container");
    let send_msg = `
    <div class="message-box from-me">
        <p class="s-text">${koreaTime}</p>
        <div class="message-text">${title}</div>
    </div>
    `
    let loading_msg = `
    <div class="message-box from-you">
        <img id="loading_img" src="/static/img/loading.gif" width="24" height="24">
    </div>
    
    `
    msg_you.innerHTML += send_msg
    msg_you.innerHTML += loading_msg


    // id가 "message-textarea"인 textarea 요소를 가져옵니다.
    let textarea = document.getElementById("message-textarea");

    // textarea의 내용을 삭제합니다.
    textarea.value = "";

    console.log(title)
    fetch('/autocomplete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: new URLSearchParams({
            'title': title
        })
    })
        .then(response => response.json())
        .then(data => {
            // document.getElementById('loading-animation').style.display = 'none';
            // document.getElementById('ai-img').style.display = 'block';
            let loadingImg = document.querySelector('.chat-container #loading_img');
            if (loadingImg) {
                loadingImg.remove();
            }

            //기존 내용에 자동완성 된 내용 더함        
            
            data.message = data.message.replace(/\n/g, '<br>');
            rep_msg = `
                        <div class="message-box from-you">
                            <div class="message-text">${data.message}</div>
                            <p class="s-text">${koreaTime}</p>
                        </div>
            `
            msg_you.innerHTML += rep_msg
            // let iframe = document.getElementById('id_content_iframe');
            // var iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
            // let notesd = iframeDocument.querySelector('.note-editable');

            // notesd.innerHTML += data.message
            // iframe.innerHTML += data.message
            
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('loading-animation').style.display = 'none';
        });


});

const messageTextarea = document.getElementById('message-textarea');

messageTextarea.addEventListener('keydown', (event) => {
if (event.key === 'Enter' && event.target.value.trim() === '/검색') {
    // 검색창 열기 또는 검색 기능 실행
    openSearchWindow(); // 검색창 열기 함수 호출
    event.preventDefault(); // Enter 키 기본 동작 막기 (개행 방지)
}
});