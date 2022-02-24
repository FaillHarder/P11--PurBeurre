const query = document.getElementById("query");
const submitQuery = document.getElementById("submitQuery");
const form = document.getElementById("form");
const body = document.getElementById("page-top");
const btn = document.getElementById("test");

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
    let formData = new FormData();
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    formData.append("query", query.value);
    form.reset()
    let result = await postQuery("ajax_search_product", formData, csrfToken);
    console.log(result["result"])
    for (let product of result["result"]) {
        console.log(product["product_name"])
    }
})

// display product

// function createDivCol() {
//     let divCol = document.createElement("div");
//     divCol.classList.add("col", "d-flex", "justify-content-center", "m-1");
//     return divCol;
// }

// function createDivCard() {
//     let divCard = document.createElement("div");
//     divCard.classList.add("card", "prod_card");
//     // divCard.style.cssText = "";
//     return divCard;
// }

// function createDivPosition() {
//     let divPosRelativ = document.createElement("div");
//     divPosRelativ.classList.add("position-relative");
//     return divPosRelativ;
// }



btn.addEventListener("click", createProductCard);

function createDiv(classlist) {
    let newDiv = document.createElement("div");
    newDiv.classList.add(...classlist);
    return newDiv;
}

const classDivCol = ["col", "d-flex", "justify-content-center", "m-1"];
const classDivCard = ["card", "prod_card"];
const classDivPosition = ["position-relative"];


function createProductCard() {
    const divCol = createDiv(classDivCol);
    const divCard = createDiv(classDivCard);
    divCol.appendChild(divCard);
    const divPosition = createDiv(classDivPosition);
    divCard.appendChild(divPosition);
    const nutriImg = createImgNutriscore("E");
    divPosition.appendChild(nutriImg);
    ajax.appendChild(divCol);
    const productImg = createImgProduct("https://fr.openfoodfacts.org/images/products/301/762/042/5035/front_fr.330.400.jpg");
    divCard.appendChild(productImg);
    const productName = createProductName("Nutella");
    divCard.appendChild(productName);
    const productLink = createProductLink("substitute?query=3242272349556");
    divCard.appendChild(productLink);
}

function createProductCard2(nutri, imgProduct, nameProduct, substitute) {
    const divCol = createDiv(classDivCol);
    const divCard = createDiv(classDivCard);
    divCol.appendChild(divCard);
    const divPosition = createDiv(classDivPosition);
    divCard.appendChild(divPosition);
    const nutriImg = createImgNutriscore(nutri);
    divPosition.appendChild(nutriImg);
    ajax.appendChild(divCol);
    const productImg = createImgProduct(imgProduct);
    divCard.appendChild(productImg);
    const productName = createProductName(nameProduct);
    divCard.appendChild(productName);
    const productLink = createProductLink(substitute);
    divCard.appendChild(productLink);
}

createProductCard2(
    "a",
    "https://fr.openfoodfacts.org/images/products/80050100/front_fr.75.400.jpg",
    "Petit Nutella",
    "substitute?query=3242272349556"
)


function createImgNutriscore(nutriscore) {
    let imgNutriscore = document.createElement("img");
    imgNutriscore.classList.add("img_nutriscore");
    let str1 = "static/assets/img/nutriscore/nutriscore-"
    let str2 = ".png"
    imgNutriscore.src = str1.concat(nutriscore, str2);
    imgNutriscore.alt = "nutriscore";
    return imgNutriscore;
}

function createImgProduct(productImg) {
    let img = document.createElement("img");
    img.src = productImg;
    img.classList.add("ajax-img");
    img.alt = "image du produit";
    return img;
}

function createProductName(productName) {
    let p = document.createElement("p");
    p.classList.add("card-text");
    p.textContent = productName;
    return p;
}

function createProductLink(link) {
    let a = document.createElement("a");
    a.classList.add("btn", "btn-primary");
    a.href = link;
    a.textContent = "Sélectionner";
    return a;
}