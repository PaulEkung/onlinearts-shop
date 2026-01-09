 // Login Form Input validation
 document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    const spinner = document.getElementById('spinner');
    const createAccountTxt = document.getElementById('trigger');
    spinner.classList.remove('d-none'); // Show the spinner
    createAccountTxt.classList.add('d-none')
    // Simulate a delay for demonstration (replace with your actual form submission logic)
    setTimeout(() => {
        spinner.classList.add('d-none'); // Hide the spinner after 5 seconds
         createAccountTxt.classList.remove('d-none')
        // Submit the form after the delay
       this.submit();
    }, 5000);
});

    const emailInput1 = document.getElementById('floatingInputInvalidEmail');

emailInput1.addEventListener('input', function(){
    const emailRegex1 = /^[a-zA-Z0-9.]+@([a-z.]*[a-z]+)$/;
    //const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex1.test(emailInput1.value);

    if (isValid) {
        emailInput1.classList.remove('is-invalid');
        emailInput1.classList.add('is-valid');
    } else {
        emailInput1.classList.remove('is-valid');
        emailInput1.classList.add('is-invalid');   

    }
});

document.getElementById("floatingInputInvalidPwd").addEventListener('input', function(){
       const input = this;
       if(input.value.length >= 6){
        input.className = 'form-control is-valid';
       } else{
        input.className = 'form-control is-invalid';
       }
    });