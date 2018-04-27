function sendToDB(){
    var inputpersonName = document.getElementById("inputpersonName").value;
    var inputEmail = document.getElementById("inputEmail").value;
    var inputCity = document.getElementById("inputCity").value;
    var inputMedName = document.getElementById("inputMedName").value;
    var inputExpirationDate =document.getElementById("inputExpirationDate").value;
    var inputAmount =document.getElementById("Amount").value;
    var isChecked =document.getElementById("gridCheck").isChecked;
    $.post( "/add", { med_name:inputMedName, date:inputExpirationDate, amount:inputAmount, is_closed:isChecked, city:inputCity, owner_mail:inputEmail, owner_name:inputpersonName });
//   .done(function( data ) {
//     alert( "Data Loaded: " + data );
//   });
}
    