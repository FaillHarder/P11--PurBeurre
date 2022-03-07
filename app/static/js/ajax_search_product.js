// const query = document.getElementById("query");
const submitQuery = document.getElementById("submitQuery");
const form = document.getElementById("form");
const body = document.getElementById("page-top");
const ajax = document.getElementById("ajax");

// requete ajax
async function postQuery(url, data, csrftoken) {
    let requestData = await fetch(url, {
        method: "POST",
        body: data,
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    let jsonData = await requestData.json()
    return jsonData
}

// search
submitQuery.addEventListener("click", async function(e) {
    e.preventDefault();
    clearResult();
    let formData = new FormData();
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let query = document.getElementById("query");
    formData.append("query", query.value);
    form.reset();
    // requeste
    let result = await postQuery("ajax_search_product", formData, csrfToken);
    // display result
    if (result["result"].length == 0) {
        const divCol = createDiv(classDivCol);
        divCol.innerHTML += "Aucun résultat";
        ajax.appendChild(divCol);
    } else {
        for (let product of result["result"]) {
            createProductCard(
                product["nutriscore"],
                product["image"],
                product["product_name"],
                product["bar_code"],
            );
        }
    }
})

// class list
const classDivCol = ["col", "d-flex", "justify-content-center", "m-4"];
const classDivCard = ["card", "prod_card", "m-auto"];
const classDivPosition = ["position-relative"];
const classImgProduct = ["card-img-top", "img_ajax"];
const classNameProduct = ["text-center", "m-auto"];
const classImgNutriscore = ["img_nutriscore"];
const classLinkProduct = ["btn", "btn-primary", "m-auto", "mb-1"];

// create product
function createProductCard(nutri, imgProduct, nameProduct, substitute) {
    const divCol = createDiv(classDivCol);
    const divCard = createDiv(classDivCard);
    divCol.appendChild(divCard);
    const divPosition = createDiv(classDivPosition);
    divCard.appendChild(divPosition);
    const nutriImg = createImgNutriscore(nutri, classImgNutriscore);
    divPosition.appendChild(nutriImg);
    const productImg = createImgProduct(imgProduct, classImgProduct);
    divCard.appendChild(productImg);
    const productName = createProductName(nameProduct, classNameProduct);
    divCard.appendChild(productName);
    const productLink = createProductLink(substitute, classLinkProduct);
    divCard.appendChild(productLink);
    ajax.appendChild(divCol);
}

function createDiv(classlist) {
    let newDiv = document.createElement("div");
    newDiv.classList.add(...classlist);
    return newDiv;
}

function createImgNutriscore(nutriscore, classlist) {
    let imgNutriscore = document.createElement("img");
    imgNutriscore.classList.add(...classlist);
    let str1 = "static/assets/img/nutriscore/nutriscore-"
    let str2 = ".png"
    imgNutriscore.src = str1.concat(nutriscore, str2);
    imgNutriscore.alt = "nutriscore";
    return imgNutriscore;
}

function createImgProduct(productImg, classlist) {
    let img = document.createElement("img");
    img.src = productImg;
    img.classList.add(...classlist);
    img.alt = "image du produit";
    return img;
}

function createProductName(productName, classlist) {
    let p = document.createElement("div");
    p.classList.add(...classlist);
    p.textContent = productName;
    return p;
}

function createProductLink(link, classlist) {
    let a = document.createElement("a");
    let substituteLink = "/substitute?query="
    a.classList.add(...classlist);
    a.href = substituteLink.concat(link);
    a.textContent = "Sélectionner";
    return a;
}

// remove product
function clearResult() {
    let productDiv = document.querySelectorAll(".col");
    productDiv.forEach(function(div) {
        div.remove();
    })
}