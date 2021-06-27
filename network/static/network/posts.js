// works -- div no form button click fetch
// adjust structure

document.addEventListener("DOMContentLoaded", () => {
    // disable page button
    disablePageButton();

    furl = document.URL.slice(document.URL.indexOf("/", 8) + 1, document.URL.indexOf("/", 8) + 1 + 5)
    if (furl !== "posts" && furl !== "users" && furl !== "login" && furl !== "logou" && furl !== "regis"){
        window.location.replace("");
    }

    // change pages when clicking pages numbers
    document.querySelectorAll("#pagesdiv button").forEach(button => {
        button.addEventListener("click", () => {
            let num = button.innerHTML;
            
            window.location.href = `page${num}`;
        })
    });

    // count textarea chars and alert when >= 270
    if (document.querySelector(".newpost textarea")){
        countchars(document.querySelector(".newpost textarea"));
    }

    // edit post
    document.querySelectorAll(".edit").forEach(item => {
        item.addEventListener("click", () => {
            if ( user == item.parentElement.dataset.user && item.nextElementSibling.nextElementSibling.style.display != "none"){
                let text = item.nextElementSibling.nextElementSibling;
                text.style.display = "none";
                item.style.color = "black";
            
                let newform = createform();
            
                let p = item.parentElement;
                p.insertBefore(newform, p.querySelector(".date").previousElementSibling);
            
                countchars(newform.querySelector("textarea"));
            }
        });
    });

    // like and unlike
    document.querySelectorAll("img").forEach( img => {
        img.addEventListener("click", () => {
            if (user){
                let like;
                let f = img.src.lastIndexOf("/") + 1;
                if( img.src.slice(f) === "unliked.png") {
                    img.src = img.src.slice(0, f) + "liked.png";
                    like = true;
                    let text = img.nextElementSibling.innerHTML.replaceAll(" ", "");
                    img.nextElementSibling.innerHTML = "   " + (parseInt(text) + 1);
                }
                else {
                    img.src = img.src.slice(0, f) + "unliked.png";
                    like = false;
                    let text = img.nextElementSibling.innerHTML.replaceAll(" ", "");
                    img.nextElementSibling.innerHTML = "   " + (parseInt(text) - 1);
                }

                fetch("/likepost", {
                    method: "PUT",
                    mode: "same-origin",
                    credentials: "include", 
                    headers : {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrf
                    },
                    body: JSON.stringify({
                        like: like,
                        id: img.dataset.id
                    })

                });
            }
        })
    });

    document.querySelector("#follow").addEventListener("click", (Event) => {
        var button = document.querySelector("#follow");
        var follow;
        let firsttext = document.querySelector("#followers").innerHTML.slice(0,11);
        let num = parseInt(document.querySelector("#followers").innerHTML.slice(11));
        if (button.innerHTML === "Follow"){
            follow = true;
            button.innerHTML = "Unfollow";
            num ++;
        }
        else {
            follow = false;
            button.innerHTML = "Follow";
            num --;
        }
        document.querySelector("#followers").innerHTML = firsttext.concat(num);

        fetch("/followuser", {
            method: "PUT",
            mode: "same-origin",
            credentials: "include",
            headers : {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-CSRFToken": csrf
            },
            body: JSON.stringify({
                follow: follow,
                pageuser: pageuser
            })
        });
    });
});

// disable page button
function disablePageButton(){
    let num = parseInt(document.URL.slice(document.URL.lastIndexOf("/") + 5));
    let x = document.querySelectorAll(`#pagesdiv button`);
    for (let e in x){
        if (x[e].innerHTML == num){
            x[e].disabled = true;
            break;
        }
    }
}

// count textarea chars and alert when >= 270
function countchars(textarea){
    textarea.addEventListener("keyup", () => {
        let value = textarea.value;
        let count = value.length;
        if (count >= 270){
            textarea.parentElement.parentElement.lastElementChild.innerHTML = `   ${280 - count} characters left`;
        }
        else {
            textarea.parentElement.parentElement.lastElementChild.innerHTML = "";
        }
    });
}


// create new form for posts and comments
function createform(){
    let spanp = document.createElement("span");

    let form = document.createElement("div");
    form.className = "newpost";
    form.style = "margin: 0px; border: none; padding: 0px;";

    let input = document.createElement("input");
    input.type = "hidden";
    /*input.name = "csrfmiddlewaretoken";
    input.value = csrf;*/
    form.appendChild(input);

    let textarea = document.createElement("textarea");
    textarea.maxLength = 280;
    form.appendChild(textarea);

    let br = document.createElement("br");
    form.appendChild(br);
    spanp.appendChild(form);

    let button = document.createElement("button");
    button.className = "btn btn-primary";
    button.innerHTML = "Save";
    button.style.marginRight = "7px";
    button.setAttribute("onclick", "save(this)");
    spanp.appendChild(button);


    button = document.createElement("button");
    button.className = "btn btn-primary";
    button.setAttribute("onclick", "cancel(this)");
    button.innerHTML = "Cancel";
    button.style.display = "inline-block";
    spanp.appendChild(button);

    let span = document.createElement("span");
    spanp.appendChild(span);

    return spanp;
}

// for the new form
function cancel(m){
    m.parentElement.previousElementSibling.style.display = "block";
    m.parentElement.previousElementSibling.previousElementSibling.previousElementSibling.style.color = "#657ff0";
    m.parentElement.remove();
}

// for the new form
function save(m){
    let value = m.previousElementSibling.querySelector("textarea").value;
    let span = m.parentElement.parentElement;
    let id = span.dataset.id;
    fetch("/editpost", {
        credentials: 'include',
        method: 'PUT',
        mode: 'same-origin',
        headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf
        },
        body: JSON.stringify({
            value: value,
            id: id,
        })
    })

    let llist = span.children;
    llist[3].style.color = "#657ff0";
    llist[5].style.display = "inline-block";
    llist[5].innerHTML = value;
    llist[6].remove();
    return false;
}