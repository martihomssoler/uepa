const ELEMENT_SELECTOR = 'selector__element'
const SECTION = 'sections__section'

const ELEMENT_SELECTED = 'selector__element-selected'
const SECTION_SELECTED = 'sections__section-selected'

document.addEventListener('DOMContentLoaded', function(e){
    renderAccordionsForMobile()
    renderHowSelector()
})

function renderAccordionsForMobile () {
    let accordions = document.getElementsByClassName('point__title')
    
    for (let i = 0; i < accordions.length; i++) {
        accordions[i].addEventListener('click', function () {
            this.classList.toggle('active')
            let panel = this.nextElementSibling
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null
            } else {
                panel.style.maxHeight = panel.scrollHeight + 'px'
            }
        })
    }
}

function renderHowSelector () {
    let howSelectors = document.getElementsByClassName(ELEMENT_SELECTOR)
    let howSections = document.getElementsByClassName(SECTION)
    
    for (let i = 0; i < howSelectors.length; i++) {
        howSelectors[i].addEventListener('click', function () {
            if (this.classList.contains(ELEMENT_SELECTED)) {
                return
            }

            for (let j = 0; j < howSelectors.length; j++) {
                howSelectors[j].classList.toggle(ELEMENT_SELECTED)
                howSections[j].classList.toggle(SECTION_SELECTED)
            }
        })
    }
}