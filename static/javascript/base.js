let user = $(".user-icon i")
let userAuth = $(".user-auth")

$(document).click(function(e) {
    let target = $(e.target)
    if(target.closest('.user-icon').length !== 0 ){
        userAuth.toggleClass("hidden")
        console.log(userAuth)
    }
    else if(!target.closest('.user-auth').length && userAuth.is(":visible")) {
        userAuth.addClass("hidden")
    }
})