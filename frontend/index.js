const pwd1 = document.getElementById('pwd1')
const pwd2 = document.getElementById('pwd2')
const cambiarPassword = document.getElementById('confirm-button')
const BACKEND_URL = 'http://127.0.0.1:5000'
const infoUsuario = document.getElementById('info-usuario')

// Asi se lee los query params en el fronted
const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
const token = urlParams.get('token')

fetch(`${BACKEND_URL}/validar-token`,{
    method: 'POST',
    body: JSON.stringify({'token':token}),
    headers:{
        'Content-Type': 'application/json'
    }
}).then((valor) => {
    console.log(valor)
    return valor.json()
}).then((data) => {
    infoUsuario.innerText = `Bienvenido ${data.content.nombre} ingresa dos veces tu nueva password para cambiarla`
    console.log(data)
}).catch((error) => {
    console.log("Hubo un error")
})

cambiarPassword.addEventListener('click', (event)=> {
    event.preventDefault()
    const valor1 = pwd1.value
    const valor2 = pwd2.value
    if(valor1!== valor2){
        alert("Las passwords no coinciden")
    }
    else{
        const body = {
            token: token,
            nuevaPassword: valor1
        }
        fetch(`${BACKEND_URL}/confirm-reset-password`,{
            method:'POST',
            body: JSON.stringify(body),
            headers:{
                'Content-Type':'application/json'
            }

        }).then((value)=>{
            return value.json()
        }).then((data)=>{
            console.log(data)
        }).catch((error) => {
            console.log(error)
        })
    
    }


}
)


