/*
=========================================
FlaskChatPro Chat JS
=========================================
*/


/*
=========================================
Chat Elements
=========================================
*/

const groupChatBox =
document.getElementById("chat-box");

const privateChatBox =
document.getElementById("private-chat-box");


/*
=========================================
Socket Connection
(Already created in base.html)
=========================================
*/

if (typeof socket === "undefined") {

    console.error("Socket not initialized.");

}
else{

    console.log("Chat Socket Ready");

}


/*
=========================================
Group Chat
=========================================
*/

if (groupChatBox && typeof socket !== "undefined") {

    socket.emit("join_group");


    socket.on("receive_group_message", function(data){

        groupChatBox.innerHTML += `

            <div class="mb-2">

                <strong>${data.sender}</strong>

                <br>

                ${data.message}

            </div>

            <hr>

        `;

        groupChatBox.scrollTop =
        groupChatBox.scrollHeight;

    });

}


/*
=========================================
Private Chat
=========================================
*/

if (privateChatBox && typeof socket !== "undefined") {

    const receiverInput =
    document.getElementById("receiver_id");

    if(receiverInput){

        socket.emit(
            "join_private",
            {
                receiver_id: receiverInput.value
            }
        );

    }


    socket.on(
        "receive_private_message",
        function(data){

            const receiverId =
            document.getElementById("receiver_id").value;

            if(
                data.sender_id != receiverId &&
                data.receiver_id != receiverId
            ){
                return;
            }

            privateChatBox.innerHTML += `

                <div class="alert alert-secondary">

                    <strong>${data.sender}</strong>

                    <br>

                    ${data.message}

                </div>

            `;

            privateChatBox.scrollTop =
            privateChatBox.scrollHeight;

        }
    );

}


/*
=========================================
Notifications
=========================================
*/

if (typeof socket !== "undefined") {

    socket.on(
        "new_notification",
        function(data){

            console.log(data);

            let badge =
            document.getElementById("notification-count");

            if(badge){

                let count =
                parseInt(badge.innerHTML || 0);

                badge.innerHTML =
                count + 1;

            }

        }
    );

}