// // Featured on CodePen's Most Hearted of 2023 list at #100
// https://codepen.io/2023/popular


// Best viewed in Full Screen mode
// https://codepen.io/jackiezen/full/oNJMOvZ

const button = document.querySelector('.filter-button');
const menu = document.querySelector('.filter-options');

menu.style.display = "none";

button.addEventListener("click", () => {
    if(menu.style.display === "none") {
        menu.style.display = "block";
        console.log('to block');
    } else {
        menu.style.display = "none";
        console.log('to none');
    }
    console.log("show");
});
