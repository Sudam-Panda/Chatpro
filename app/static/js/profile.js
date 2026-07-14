/*
===================================================
profile.js
FlaskChatPro Profile Image Preview
===================================================
*/


const imageInput =
document.getElementById(
    "profile_picture"
);



const imagePreview =
document.getElementById(
    "profile-preview"
);





if(imageInput){


    imageInput.addEventListener(
        "change",
        function(event){


            const file =
            event.target.files[0];



            if(file){


                const reader =
                new FileReader();



                reader.onload =
                function(e){


                    if(imagePreview){


                        imagePreview.src =
                        e.target.result;


                    }


                };



                reader.readAsDataURL(
                    file
                );


            }



        }
    );


}