function enableCheckboxes(checkboxIds) {

    document.querySelectorAll('.form-check-input').forEach(function (checkbox) {
        checkbox.disabled = true;
        checkbox.checked = false;
        document.querySelector(`label[for="${checkbox.id}"]`).classList.remove('for-checkbox-underline');
    });


    checkboxIds.forEach(function (checkboxId) {
        const checkbox = document.getElementById(checkboxId);
        checkbox.disabled = false;
        document.querySelector(`label[for="${checkboxId}"]`).classList.add('for-checkbox-underline');


        checkbox.addEventListener('change', function () {
            if (this.checked) {

                checkboxIds.forEach(function (id) {
                    if (id !== checkboxId) {
                        const otherCheckbox = document.getElementById(id);
                        otherCheckbox.checked = false;
                    }
                });
            }

            showNextButton();
        });
    });
}


function disableAllCheckboxes() {
    document.querySelectorAll('.form-check-input').forEach(function (checkbox) {
        checkbox.disabled = true;
        checkbox.checked = false;
        document.querySelector(`label[for="${checkbox.id}"]`).classList.remove('for-checkbox-underline');
    });
}


window.onload = function () {
    disableAllCheckboxes();
};


document.getElementById("Virtual").addEventListener("click", function () {
    enableCheckboxes(["l2-1", "l2-3", "l2-4", "l2-5", "l2-6", "l2-7", "l2-12", "l2-16", "l2-17",
        "l2-18", "l2-19", "l2-21", "l2-27", "l2-33", "l3-14", "l3-42", "l3-45", "l3-45", "l3-46",
        "l3-47", "l3-49", "sec-1", "sec-3", "sec-4", "sec-5", "sec-6", "sec-7", "sec-8", "sec-9",
        "sec-10", "sec-11", "sec-12", "mgmn-1", "mgmn-2", "mgmn-3", "mgmn-4", "mgmn-5", "mgmn-6", "mgmn-7",
        "mgmn-8", "l3-24", "l3-25", "l3-26", "l3-34", "l3-35", "l3-36", "l3-37", "l3-39", "l3-40", "l3-48", "l3-56"]);
});

document.getElementById("Physical").addEventListener("click", function () {
    enableCheckboxes(["l2-2", "l2-8", "l2-9", "l2-10", "l2-11", "l2-13", "l2-22", "l2-23", "l2-24",
        "l2-30", "l2-31", "l2-34", "l2-35", "l2-36", "l2-37", "l3-2", "l3-3", "l3-15", "l3-16", "l3-27",
        "l3-28", "l3-29", "l3-30", "l3-31", "l3-32", "l3-33", "l3-38", "l3-50", "l3-51", "l3-52",
        "l3-53", "l3-54", "l3-55", "sec-2", "l2-15", "l2-25", "l2-26", "l2-28", "l2-29", "l2-32", "l2-38", "l2-39", "l3-1",
        "l3-2", "l3-4", "l3-5", "l3-6", "l3-7", "l3-8", "l3-9", "l3-10", "l3-11", "l3-13",
        "l3-17", "l3-18", "l3-19", "l3-20", "l3-21", "l3-22",]);
})
;


function showNextButton() {

    const anyCheckboxChecked = Array.from(document.querySelectorAll('.form-check-input'))
        .some(checkbox => checkbox.checked);
    document.getElementById("nextButton").style.display = anyCheckboxChecked ? "block" : "none";
}

document.addEventListener('DOMContentLoaded', showNextButton);
