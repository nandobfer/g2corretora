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

$(".radios").on("change", get_person);

rcpf.prop("checked", true).change();