/*
===================================================
typing.js
FlaskChatPro Typing Indicator
===================================================
*/


const socketTyping = io();



// ===================================================
// Group Chat Typing
// ===================================================


const messageInput =
document.getElementById(
    "message"
);



if(messageInput){


    messageInput.addEventListener(
        "input",
        function(){


            socketTyping.emit(
                "typing",
                {

                    typing:true

                }
            );


        }
    );


}




// ===================================================
// Private Chat Typing
// ===================================================


const privateInput =
document.getElementById(
    "private-message"
);



if(privateInput){


    privateInput.addEventListener(
        "input",
        function(){


            let receiver =
            document.getElementById(
                "receiver_id"
            ).value;



            socketTyping.emit(
                "private_typing",
                {

                    receiver_id: receiver,

                    typing:true

                }
            );



        }
    );

}



// ===================================================
// Show Typing Message
// ===================================================


socketTyping.on(
    "user_typing",
    function(data){


        let typingBox =
        document.getElementById(
            "typing-status"
        );



        if(typingBox){


            if(data.typing){


                typingBox.innerHTML =
                "Someone is typing...";


            }

            else{


                typingBox.innerHTML =
                "";


            }


        }


    }

);



// ===================================================
// Remove Typing Text
// ===================================================


let typingTimeout;


function stopTyping(){


    clearTimeout(
        typingTimeout
    );


    typingTimeout =
    setTimeout(
        function(){


            socketTyping.emit(
                "typing",
                {

                    typing:false

                }
            );


        },
        1000
    );

}


if(messageInput){


messageInput.addEventListener(
    "keyup",
    stopTyping
);


}


if(privateInput){


privateInput.addEventListener(
    "keyup",
    stopTyping
);


}