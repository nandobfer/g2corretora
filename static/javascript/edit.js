const urlParams = new URLSearchParams(window.location.search);
const cadastro_id = urlParams.get('id');
let data = urlParams.get('data');
// substituindo aspas simples por aspas duplas em toda a string
data = data.replaceAll(`'`, `"`);
// substituindo o None do python para o null do javascript
data = data.replaceAll(`None`, `null`);
// transformando a string em json (objeto)
data = JSON.parse(data);

console.log(data);

const rcpf = $("#radio-cpf");

const get_person = () => {
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

const edit_on = () => {
    $(".editions-container").removeClass("off");
}

const edit_off = () => {
    $(".editions-container").addClass("off");
}

const build_profile = () => {
    data_fields = $('.data-cadastro')
    for (let field of data_fields) {
        const id = $(field).attr('id')
        const value = data[id.slice(5)]
        if (value) {
            $(field).text(value)
        } else {
            $(field).text('-')
        }
    }
}

$(".radios").on("change", get_person);

$(".edit-button").on("click", edit_on);

$(".save-button").on("click", edit_off);

rcpf.prop("checked", true).change();

build_profile();