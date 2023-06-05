var descriptionElement = document.getElementById('description');
var seeMoreLink = document.getElementById('see-more');
var maxLength = 200;

var fullDescription = seeMoreLink.value;

if (fullDescription.length > maxLength) {

    var partialDescription = fullDescription.slice(0, maxLength) + "...";
    descriptionElement.textContent = partialDescription;
    seeMoreLink.style.display = 'inline';
} else {

    descriptionElement.textContent = fullDescription;
    seeMoreLink.style.display = 'none';
}
function showMore()
    {
        descriptionElement.textContent = fullDescription;
        seeMoreLink.style.display = 'none';
    }
async function refresh()
    {
        location.reload();
    }

function login()
    {
        loginForm = document.getElementById('loginForm');
        var formData = new FormData(loginForm);

        fetch("/login", { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                if (data.message == "Error") 
                    {
                        error = document.getElementById('logErrorMessage');
                        error.innerText = "Wrong Informations";
                        loginForm.reset();
                    }
                else 
                    {
                        window.location.replace('/dashboard');
                    }
            });
    }

function register()
    {
        regForm = document.getElementById('registrationForm');
        var formData = new FormData(regForm);
        fetch("/users/create", { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => 
            {
            error = document.getElementById('regErrorMessage');
            error.innerHTML = ""
            if (data.errors != 'success'){
                for (key in data.errors) {
                    error.innerHTML += data.errors[key] + '<br>';
                    if (data.errors[key] == "First Name must contain at least 2 characters"){
                        field = document.getElementById('first_name');
                        // field.value = "";
                        field.style.backgroundColor = "lightcoral";
                    }
                    if (data.errors[key] == "Last Name must contain at least 2 characters"){
                        field = document.getElementById('last_name');
                        // field.value = "";
                        field.style.backgroundColor = "lightcoral";
                    }
                    if (data.errors[key] == "Email Already Exists" || data.errors[key] == "Email not valid"){
                        field = document.getElementById('email');
                        // field.value = "";
                        field.style.backgroundColor = "lightcoral";
                    }
                    if (data.errors[key] == "This Email is Blacklisted"){
                        field = document.getElementById('email');
                        regForm.reset();
                        break;
                    }
                    if (data.errors[key] == "Password Must Have More Than 8 Characters" || data.errors[key] == "Password Must Contain At Least A Number And An Uppercase Character"){
                        field = document.getElementById('password');
                        field.value = "";
                        field.style.backgroundColor = "lightcoral";
                        field = document.getElementById('confirm_password');
                        field.value = "";
                    }
                    if (data.errors[key] == "Password and Confirmation Doesn't Match"){
                        field = document.getElementById('confirm_password');
                        field.value = "";
                        field.style.backgroundColor = "lightcoral";
                    }
                }
            }
            else {
                window.location.replace('/dashboard');
            }
        });
    }

function validateBook(){
    loginForm = document.getElementById('addBookForm');

    var formData = new FormData(loginForm);

    fetch("/books/create", { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => 
            {
                error = document.getElementById('addBookErrorMessage');
                error.innerHTML = ""
                if (data.errors.length !=0){
                    for (key in data.errors) {
                        error.innerHTML += data.errors[key] + '<br>';
                        if (data.errors[key] == "Book Must Have a Title"){
                            field = document.getElementById('title');
                            // field.value = "";
                            field.style.backgroundColor = "lightcoral";
                        }
                        if (data.errors[key] == "Author must contain at least 2 characters"){
                            field = document.getElementById('author');
                            // field.value = "";
                            field.style.backgroundColor = "lightcoral";
                        }
                        if (data.errors[key] == "Description must contain at least 5 characters"){
                            field = document.getElementById('description');
                            // field.value = "";
                            field.style.backgroundColor = "lightcoral";
                        }
                    }
                }
                else {
                    window.location.replace('/dashboard');
                }
            })
}

function updateBook(element)
    {
        updateForm = document.getElementById('updateBookForm');

        var formData = new FormData(updateForm);

        let book_id = element.value;
        fetch("/books/"+book_id+"/update", { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            error = document.getElementById('updateBookError');
            error.innerHTML = ""
            if (data.errors.length !=0){
                for (key in data.errors) {
                    error.innerHTML += data.errors[key] + '<br>';
                    if (data.errors[key] == "Book Must Have a Title"){
                        field = document.getElementById('title');
                        field.style.backgroundColor = "lightcoral";
                    }
                    if (data.errors[key] == "Author must contain at least 2 characters"){
                        field = document.getElementById('author');
                        field.style.backgroundColor = "lightcoral";
                    }
                    if (data.errors[key] == "Description must contain at least 5 characters"){
                        field = document.getElementById('description');
                        field.style.backgroundColor = "lightcoral";
                    }
                }
            }
            else {
                window.location.replace('/dashboard');
            }
        })
    }

function createLike(element) {
    let book_id = element.value;
    fetch("/likes/" + book_id + "/create")
        .then(response => response.json())
        .then(data => {
            // let newElement = document.createElement("span");
            // newElement.innerHTML = "This is one of your favorites";
            // newElement.classList.add("fst-italic");
            // element.replaceWith(newElement);
            count = parseInt(document.getElementById('count').innerText);
            document.getElementById('count').innerText = count + 1;
        })
    setTimeout(() => {
        location.reload();
    }, 500);
}

function deleteLike(element)
    {
        let book_id = element.value;
        fetch("/likes/"+book_id+"/delete")
        .then(response => response.json())
        .then(data => {
            if (data.message){
                parent = element.parentNode;
                parent.remove();
                element.remove();
                count = parseInt(document.getElementById('count').innerText);
                document.getElementById('count').innerText = count-1;
            }
        })
    }
function deleteLikeReload(element) {
    let book_id = element.value;
    fetch("/likes/" + book_id + "/delete")
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                // parent = element.parentNode;
                // parent.remove();
                // element.remove();
                count = parseInt(document.getElementById('count').innerText);
                document.getElementById('count').innerText = count - 1;
            }
        })
        setTimeout(() => {
            location.reload();
        }, 500);
}

async function getBookInfo(element)
    {
        let book_id = element.getAttribute("data-value1");
        let book_title = element.getAttribute("data-value2");
        let book_author = element.getAttribute("data-value3");
        let api_key = "AIzaSyBRG1XH1T46NTFw3FnL9IhrevoXpuTAdhA";
        let response = await fetch("https://www.googleapis.com/books/v1/volumes?q=intitle:"+book_title+"+inauthor:"+book_author+"&key="+api_key);
        let data = await response.json();
        // console.log(data);
        try {
            apiData = data.items[0].volumeInfo;
            first_publish_year = apiData.publishedDate;
            if (apiData.averageRating) {
                rating = apiData.averageRating.toPrecision(3);
            }
            else {
                rating = "N/A";
            }
            categories = apiData.categories;
            try {
                imgSrc = apiData.imageLinks.thumbnail;
            }
            catch
            {
                imgSrc = "/static/img/404-page-not-found.webp"
            }
        }
        catch {
            first_publish_year = "N/A";
            rating = "N/A";
            categories = ["N/A"];
            imgSrc = "/static/img/404-page-not-found.webp";
        }
        
        data = {
            'first_publish_year' : first_publish_year,
            'rating' : rating,
            'categories' : categories,
            'imgSrc' : imgSrc
        }
    fetch("/books/api", {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
        .then(data => {
            window.location.replace("/books/"+book_id+"/view");
            // console.log("DATA : ", data);
        });
}

async function getAuthorInfo(element) {
    let book_author = element.getAttribute("data-value3");
    let response = await fetch("https://openlibrary.org/search.json?author=" + book_author);
    let data = await response.json();
    author_key = data.docs[0].author_key[0];
    fetch(`https://openlibrary.org/authors/${author_key}.json`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            img = data.key.split("/")[2];
            console.log(img);
            try{
                imgSrc = "https://covers.openlibrary.org/a/olid/"+img+"-L.jpg";
            }
            catch{
                imgSrc = "/static/img/404-page-not-found.webp";
            }
            try{
                bio = data.bio.split("([Source")[0];
            }
            catch{
                bio = "Biography not available for "+book_author;
            }
            name = data.name;
            try{
                link = data.links[0].url;
            }
            catch{
                link = data.wikipedia;
            }
            try{
                alternate_names = [data.alternate_names[0], data.alternate_names[1]];
            }
            catch{
                alternate_names = []
            }
            birth_date = data.birth_date;
            try {
                death_date = data.death_date;
            }
            catch{
                death_date = "";
            }
            data = {
                'alternate_names': alternate_names,
                'link': link,
                'birth_date': birth_date,
                'death_date': death_date,
                'bio': bio,
                'name': name,
                'imgSrc': imgSrc
            }
            fetch("/authors/api", {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => response.json())
                .then(data => {
                    window.location.replace("/authors/view");
                });
        });
}

function addComment()
    {
        commentForm = document.getElementById('formComment');
        var formData = new FormData(commentForm);

        fetch("/comments/create", { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                if (data.status == "Fail") 
                    {
                        errorField = document.getElementById('commentErrorMessage');
                        errorField.innerText = "Comment must contain at least 5 characters";
                        commentField =document.getElementById('area_comment');
                        commentField.style.backgroundColor = "lightcoral";
                    }
                else 
                    {
                        window.location.replace('/books/'+data.status+'/view');
                    }
            });
    }

function editComment(element)
    {
        idComment = element.value;
        content = element.parentNode.parentNode.innerText;
        newInput = document.createElement("input");
        newInput.setAttribute("type", "text");
        newInput.classList.add("form-control");
        newInput.classList.add("form-control-sm");
        newInput.value = content;
        newButton = document.createElement('button');
        newButton.setAttribute("value", idComment);
        newButton.classList.add("btn");
        newButton.classList.add("btn-outline-success");
        newButton.setAttribute("onclick", "changeComment(this)");
        newButton.innerHTML = "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-check' viewBox='0 0 16 16'><path d='M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z'/></svg>";
        grandParent = element.parentNode.parentNode;
        grandParent.replaceWith(newInput);
        newInput.classList.add('mb-2');
        newInput.insertAdjacentElement('afterend', newButton);
    }

function changeComment(element) {
    idComment = element.value;
    content = element.previousSibling.value;
    url = "/comments/" + idComment + "/edit/" + content;
    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Erreur : ' + response.status);
            }
        })
        .then(data => {
            console.log(data.status);
            if (data.status == 'Fail') {
                element.previousSibling.style.backgroundColor = "lightcoral";
                element.previousSibling.value = content;

            }
            else {
                window.location.replace('/books/' + data.status + '/view')
            }

        }).catch(error => {
            element.previousSibling.style.backgroundColor = "lightcoral";
            element.previousSibling.value = content;
        });
}

    