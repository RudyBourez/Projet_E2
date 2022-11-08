const rangeResults = document.querySelectorAll('.range-result')

rangeResults.forEach(function(rangeResult) {
    const rangeInput = document.querySelector('#' + rangeResult.dataset.input);

    if (rangeInput) {
        rangeResult.innerHTML = rangeInput.value + " / 10";

        rangeInput.addEventListener('input', function() {
            rangeResult.innerHTML = rangeInput.value + " / 10";
        });
    }
});

const Bsmt_Qual = document.querySelector('.Bsmt_Qual')
const LiBsmt_Qual = document.querySelector('#LiBsmt_Qual')

Bsmt_Qual.addEventListener('mouseenter', function (){
    LiBsmt_Qual.style.display = 'block';
})
Bsmt_Qual.addEventListener('mouseleave', function (){
    LiBsmt_Qual.style.display = 'none';
});

const Age_house = document.querySelector('.Age_house')
const LiAge_house = document.querySelector('#LiAge_house')

Age_house.addEventListener('mouseenter', function (){
    LiAge_house.style.display = 'block';
})
Age_house.addEventListener('mouseleave', function (){
    LiAge_house.style.display = 'none';
});