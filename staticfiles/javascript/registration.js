$.ajax({
    type:"get",
    url: `/api/user/`,
    dataType:'json',
    success: function(data) {
        returnData(data);
    }
})

function returnData(data){
	let email = []
	for (i of data) 
		email.push(i.email)
	$("form").submit(email, validate)
}

function validate(e) {
	emailField = $(this).find("input[type=email]")
	password1 = $(this).find("input[name=password1]")
	password2 = $(this).find("input[name=password2]")


	if ((e.data).includes(emailField.val()) || (password1.val().length < 8) || (password1.val() !== password2.val())) {
		e.preventDefault()

		$(this).find(".validate-text").remove()
		$(this).find(".validate").removeClass("validate")

		console.log($(this).find(".validate-text"))
		console.log($(this).find(".validate"))

		if ((e.data).includes(emailField.val())) {
			emailField.addClass("validate")
			emailField.after(
					`<p class="validate-text">Email already taken.</p>`
				)
		}

		if (password1.val().length < 8) {
		
			password1.addClass("validate")
			password1.after(
					`<p class="validate-text">Password must have more than 8 character.</p>`
				)
		}

		if (password1.val() !== password2.val()) {
			
			password1.addClass("validate")
			password2.addClass("validate")
			password2.after(
					`<p class="validate-text">Password did not match.</p>`
				)

		}

		return false
	}
}