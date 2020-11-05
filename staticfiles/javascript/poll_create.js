
let add = $("#add-btn");
add.on("click", handleAdd);

let form = $("#option-form");

let manageForm = $("#id_form-TOTAL_FORMS");
let inputId = 2;
let id = inputId + 1;

function handleAdd(e) { 
	if (inputId < 4) {

		let content = `<label for="id_form-${inputId}-option">Option ${inputId + 1}</label>
						<input
							type="text"
							name="form-${inputId}-option"
							maxlength="200"
							id="id_form-${inputId}-option"
							class="input-box"/>
						<input type="hidden" name="form-${inputId}-id" id="id_form-${inputId}-id" />`

		form.append(content)

  		inputId += 1;
  		manageForm.val(String(inputId));

  		let icon = $("#add-btn i")
		if (inputId >= 4) add.css("visibility","hidden") 
  	};
}

