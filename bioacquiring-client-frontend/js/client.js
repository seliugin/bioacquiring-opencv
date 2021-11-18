function sendRegData(reg_form) {
    return;
}

function getRegCamScreen() {
    fname = document.getElementById('fname').value;
    lname = document.getElementById('lname').value;
    tname = document.getElementById('tname').value;
    bcard = document.getElementById('bankCard').value;
    phone = document.getElementById('phone').value;
    setTimeout(()=>{setScreen(getStartScreen)}, 20000)
    return `<img src="http://10.206.0.202:8080/stream?mode=registration&fname=${fname}&&lname=${lname}&tname=${tname}&bcard=${bcard}&phone=${phone}">`
}

function getProcCamScreen() {
    setTimeout(()=>{setScreen(getStartScreen)}, 20000)
    return `<img src="http://10.206.0.202:8080/stream?mode=processing">`
}

function getProcessingScreen() {
    return `<div class="dot-bricks load-anim"></div>
        <h1>Происходит...</h1>`
}

function getStartScreen() {
    return `<div style="position: absolute; top: 45%; left: 38%">
        <a onclick="setScreen(getProcCamScreen)" class="btn btn-lg btn-secondary mg10">Оплатить</a>
        <a onclick="setScreen(getRegScreen)" class="btn btn-lg btn-secondary mg10" style="margin-left: 20px">Регистрация</a>
        </div>`
}

function getRegisterAwaitScreen() {
    return `<h1 class="cover-heading">Ждем ответа ЕБС</h1>`
}

function getIdentityScreen(name, picture, birth_date) {
    return `<div>
                <div style="display: inline-block; margin-right: 20px;">
                    <img src="${picture}" class="avatar-picture">
                </div>
                <div style="display: inline-block">
                    <h2 class="cover-heading">${name}</h2>
                    <p style="text-align: left;">Дата рождения: ${birth_date}</p>
                </div>
            </div>`
}

function getRegScreen(){
    return `<div>
                <div style="display: inline-block">
                <form id="reg-form" onsubmit="sendRegdata(this);setScreen(getRegCamScreen);">
                    <p class="a" style="text-align: left;">
                    <input id="fname" placeholder="Имя">
                    <input id="lname" placeholder="Фамилия">
                    <input id="tname" placeholder="Отчество">
                    <input id="phone" placeholder="Номер телефона">
                    <input id="bankCard" placeholder="Банковская карта">
                    </p>
                </form>
                <a onclick="setScreen(getRegCamScreen)" class="btn btn-lg btn-secondary mg10" style="margin-left: 20px">Регистрация</a>

                </div>
            </div>`
}

function setScreen(func, params = []) {
    window.root.innerHTML = func(...params);
}