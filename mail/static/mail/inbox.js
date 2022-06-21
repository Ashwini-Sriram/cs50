document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click',compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector("#email_id-view").style.display = "none";


  // Clear out composition fields

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
  
}
function reply_email(recipients,subject,body,timestamp)
{
  document.querySelector("#emails-view").style.display = "none";
   document.querySelector("#compose-view").style.display = "block";
   document.querySelector("#email_id-view").style.display = "none";
let bod=decodeURIComponent(body)
let sub=decodeURIComponent(subject)
let body_s=`On ${timestamp} , ${recipients} wrote : ${bod}`
if(!sub.startsWith("Re :")){
  sub_s = `Re : ${sub}`; 
}
else{
  sub_s = sub; 

}
 document.querySelector("#compose-recipients").value = recipients;
 document.querySelector("#compose-subject").value = sub_s;
 document.querySelector("#compose-body").value = body_s;
 console.log("hi");
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector("#email_id-view").style.display = "none";


  // Show the mailbox name
 document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
 if(mailbox=="sent")
 {
  fetch("/emails/sent")
    .then((response) => response.json())
    .then((emails) => {
      // Print emails
        let block="<table style='border:solid; width:100%'>";
                    block += `<tr  style='border:solid;'> <th>Recepient</th> <th>Subject</th> <th>Time Stamp</th> </tr>`;

     for (let x=0;x<emails.length;x++)
     {
  
      email=emails[x];
      id=email.id;
      recipients=email.recipients;
      subject = decodeURIComponent(email.subject);
      body = decodeURIComponent(email.body);
      
      read = email.read;
      timestamp =email.timestamp;


              block += line_element(id,
                 recipients,
                 subject,
                 timestamp,
                 read
               );


     }
      block+="</table>";
        document.querySelector("#emails-view").innerHTML += block ;
  
      console.log(emails);

      // ... do something else with emails ...
    });
 }
 else if (mailbox=="inbox"){
  {
  fetch("/emails/inbox")
    .then((response) => response.json())
    .then((emails) => {
      // Print emails
    
        let block="<table style='border:solid; width:100%'>";
           block += `<tr  style='border:solid;'> <th>Sender</th> <th>Subject</th> <th>Time Stamp</th> </tr>`;

      
     for (let x=0;x<emails.length;x++)
     {
    
     
      email=emails[x];
      id=email.id;
      sender=email.sender;
      subject = decodeURIComponent(email.subject);
      body = decodeURIComponent(email.body);
      read = email.read;
      timestamp =email.timestamp;

              block += line_element(id,
                 sender,
                 subject,
                 timestamp,
                 read,
               );


     }
      block+="</table>";
        document.querySelector("#emails-view").innerHTML += block ;
  
      console.log(emails);

      // ... do something else with emails ...
    });
 }

}
else if (mailbox=="archive")
{
fetch("/emails/archive")
  .then((response) => response.json())
  .then((emails) => {
    // Print emails
    console.log(emails);
    let block = "<table style='border:solid; width:100%'>";
    block += `<tr  style='border:solid;'> <th>Sender</th> <th>Subject</th> <th>Time Stamp</th> </tr>`;

    for (let x=0;x<emails.length;x++)
     {
    
     
      email=emails[x];
      id=email.id;
      sender=email.sender;
      subject = decodeURIComponent(email.subject);
      body = decodeURIComponent(email.body);
      read = email.read;
      timestamp =email.timestamp;

              block += line_element(id,
                 sender,
                 subject,
                 timestamp,
                 read
               );


     }
       block+="</table>";
        document.querySelector("#emails-view").innerHTML += block ;


    // ... do something else with emails ...
  });
}
}





function send_mail(){
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: document.querySelector("#compose-recipients").value,
      subject: encodeURIComponent(document.querySelector("#compose-subject").value),
      body: encodeURIComponent(document.querySelector("#compose-body").value),
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      // Print result
      console.log(result);
    });

    load_mailbox("Sent")

}

function line_element(id,p_rec_send,p_subject,p_timestamp,read)
{
  if(read){
  var block = `<tr onclick='each_email(${id})' style='border:solid; background-color:grey;'> <td>${p_rec_send}</td> <td>${p_subject}</td> <td '>${p_timestamp}</td> </tr>`;
  }else
  {
  var block = `<tr onclick='each_email(${id})' style='border:solid;'> <td>${p_rec_send}</td> <td>${p_subject}</td> <td '>${p_timestamp}</td> </tr>`;
  }
  return block;
}



function each_email(id)
{
   document.querySelector("#emails-view").style.display = "none";
   document.querySelector("#compose-view").style.display = "none";
   document.querySelector("#email_id-view").style.display = "block";
  
  fetch("/emails/"+id)
    .then((response) => response.json())
    .then((email) => {
      // Print email
      sender = email.sender;
      subject = decodeURIComponent(email.subject);
      body = decodeURIComponent(email.body);
      subject_nd = email.subject;
      body_nd = email.body;
      timestamp = email.timestamp;
      recipients = email.recipients;
      archive_status=email.archived;
  
      if(archive_status){
          perform = "Unarchive"
      }
      else{
          perform ="Archive"
      }
      let block = ` <hr><button value='${perform}' onclick='archive_mail(${id},${archive_status})' style='float:right;'>${perform}</button>`;
       block += `
      <div style='width:100%' style='float:left;'>
      To:${recipients} 
      <br>
      From:${sender}
      <br>
      Subject:${subject}
      <br>
      Time Stamp:${timestamp}
      <br>
      </div>
       <button value='Reply' onclick='reply_email("${sender}","${subject_nd}","${body_nd}","${timestamp}")'>Reply</button>
       <hr>`;
       

      document.querySelector("#email_id-view").innerHTML = block;
      
  
      console.log(email);
      // ... do something else with email ...
      fetch("/emails/"+id, {
        method: "PUT",
        body: JSON.stringify({
          read: true,
        }),
      });
    });
}

function archive_mail(id,status)
{
   if(status){
     set= false;
     message="Unarchived"
      }
      else
      {
       set =true;
        message = "Archived";
      }
   fetch("/emails/"+id, {
     method: "PUT",
     body: JSON.stringify({
    
      archived : set,
     }),
   });
   console.log("Archived");
   alert(message);
}
