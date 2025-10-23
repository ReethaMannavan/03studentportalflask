function validateForm() {
    const name = document.getElementById("name").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const course = document.getElementById("course").value;

    const nameRegex = /^[A-Za-z\s]+$/;
    const phoneRegex = /^[0-9]{10}$/;

    if (!nameRegex.test(name)) {
        alert("Name must contain only letters and spaces.");
        return false;
    }
    if (!phoneRegex.test(phone)) {
        alert("Phone number must be exactly 10 digits.");
        return false;
    }
    if (!course) {
        alert("Please select a course.");
        return false;
    }
    return true;
}
