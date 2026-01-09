   
 // Signup Form Input validation
    document.getElementById("floatingInputInvalidFirst").addEventListener('input', function(){
       const input = this;
       if(input.value.length > 2){
        input.className = 'form-control is-valid';
       } else{
        input.className = 'form-control is-invalid';
       }
    });

document.getElementById("floatingInputInvalidLast").addEventListener('input', function(){
       const input = this;
       if(input.value.length > 2){
        input.className = 'form-control is-valid';
       } else{
        input.className = 'form-control is-invalid';
       }
    });

document.getElementById("floatingInputInvalidPhone").addEventListener('input', function(){
    const input = this;
    // Nigerian phone: 11 digits starting with 0 OR 13 digits starting with +234
    const phoneRegex = /^(0\d{10}|\+234\d{10})$/;
    if (phoneRegex.test(input.value.trim())) {
        input.className = 'form-control is-valid';
    } else {
        input.className = 'form-control is-invalid';
    }
});

const emailInput = document.getElementById('floatingInputInvalidEmail2');

emailInput.addEventListener('input', () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    //const emailRegex = /^[a-zA-Z0-9.]+@([a-z.]*[a-z]+)$/;
    const isValid = emailRegex.test(emailInput.value);

    if (isValid) {
        emailInput.classList.remove('is-invalid');
        emailInput.classList.add('is-valid');
    } else {
        emailInput.classList.remove('is-valid');
        emailInput.classList.add('is-invalid');   

    }
});

 document.getElementById("exampleFormControlTextarea").addEventListener('input', function(){
       const input = this;
       if(input.value.length > 3){
        input.className = 'form-control is-valid';
       } else{
        input.className = 'form-control is-invalid';
       }
    });
 document.getElementById("floatingInputInvalidPwd1").addEventListener('input', function(){
       const input = this;
       if(input.value.length >= 8){
        input.className = 'form-control is-valid';
       } else{
        input.className = 'form-control is-invalid';
       }
    });

document.getElementById("floatingInputInvalidPwd2").addEventListener('input', function(){
       const input = this;
       if(input.value.length >= 8){
        input.className = 'form-control is-valid';
       } else{
        input.className = 'form-control is-invalid';
       }
    });
document.getElementById("role").addEventListener('input', function(){
       const input = this;
       if(input.value.length >= 0 ){
        input.className = 'form-control is-valid';
       } else{
        input.className = 'form-control is-invalid';
       }
    });


    

        document.getElementById('register-form').addEventListener('submit', function(event) {
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