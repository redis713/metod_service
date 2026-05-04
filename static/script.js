function confirmAck() {

    const modal = document.getElementById("modal");

    const message = document.getElementById("modal-message");

    const yesA = document.getElementById("yes-a");

    const noBtn = document.getElementById("no-btn");

    message.innerText =
        "Вы уверены, что ознакомились с методичкой?";

    yesA.onclick = function () {
        //window.location.href = url;
        document.getElementsByClassName("galochka_form")[0].submit();
    };

    modal.style.display = "flex";

    noBtn.onclick = function () {
        modal.style.display = "none";
    };
}

function delete_metod() {

    const modal = document.getElementById("modal");

    const message = document.getElementById("modal-message");

    const yesA = document.getElementById("yes-a");

    const noBtn = document.getElementById("no-btn");

    message.innerText =
        "Вы уверены, что хотите удалить методическую разработку?";

     modal.style.display = "flex";
    yesA.onclick = function () {
        console.log("Закрыли удаление");
        document.getElementById("delete_form").submit();
    };


    noBtn.onclick = function () {
        console.log("Закрыли удаление");
        modal.style.display = "none";
    };
}

function change_metod() {

    const modal = document.getElementById("modal");

    const message = document.getElementById("modal-message");

    const yesA = document.getElementById("yes-a");

    const noBtn = document.getElementById("no-btn");

    message.innerText = "Вы уверены, что хотите внести изменения в методическую разработку?";

    yesA.onclick = function () {
        document.getElementById("change_form").submit();
    };

    modal.style.display = "flex";

    noBtn.onclick = function () {
        modal.style.display = "none";
    };
}