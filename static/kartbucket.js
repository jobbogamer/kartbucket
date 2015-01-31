
function prepareEditModal(trackID, trackName, personID, personName, character, kart, wheels, glider)
{
    $("#edit-modal .modal-title").html("Add Time - " + trackName);
    $("#edit-modal-person-field").val(personID);
    $("#edit-modal-character-field").val(character);
    $("#edit-modal-kart-field").val(kart);
    $("#edit-modal-wheels-field").val(wheels);
    $("#edit-modal-glider-field").val(glider);
}
