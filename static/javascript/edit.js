const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get('id');
let data = urlParams.get('data');
data = data.split(",");

data[0] = data[0].split("[")[1];
data[data.length - 1] = data[data.length - 1].split("]")[0];

console.log(data);

const rcpf = $("#radio-cpf");

var get_person = () => {
    const person = $(".radios:checked");
    const id = person.attr("id");

    if (id == "radio-cpf") {
        $(".empresa").hide();
        $(".pessoa-fisica").show();
    } else if (id == "radio-cnpj") {
        $(".pessoa-fisica").hide();
        $(".empresa").show();
    }
}

var edit_on = () => {
    $(".editions-container").removeClass("off");
}

var edit_off = () => {
    $(".editions-container").addClass("off");
}

var build_profile = () => {
    $("#nome-da-empresa").text(data[1]);
    $("#nome-do-representante").text(data[2]);
}

$(".radios").on("change", get_person);

$(".edit-button").on("click", edit_on);

$(".save-button").on("click", edit_off);

rcpf.prop("checked", true).change();

build_profile();