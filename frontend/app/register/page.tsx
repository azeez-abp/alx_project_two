'use client'
import Button from "@/components/Button";
import { useState } from "react";
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { backend_path, makeRequest } from "../../request";

const spinner_style = {
  position: 'absolute',
  left: '17em',
  top: '-18px'
}

const form_style = {
  boxShadow: '0 4px 20px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
  padding: '1.3em',
  borderRadius: '13px'
}

const show_password_style = {
  right: '2px',
  width: 'fit-content',
  background: '#444',
  top: '2px',
  padding: '5px',
  lineHeight: '1.4',
  cursor:"pointer"
}

const Register = () => {
  const router = useRouter()
  const [loginState, setLoginState]  = useState({
   showLoader:false,
   error:false, 
   info:"", 
   inputData:{
    "email": "",
    "password": "",
    "first_name": "",
    "middle_name": "",
    "last_name": "",
    "date_of_birth": "",
    "state": "",
    "city": "",
    "street": "",
    "profile_image": "",
    "gender": "",
    "zip_code": "2000525"
},
   suc:false,
   showPassword: false

  })
  
  const disble_button = {
    pointerEvents: loginState.showLoader ? 'none' : 'all',
   opacity:loginState.showLoader ? '0.4' : '1',
   cursor:loginState.showLoader? 'none' : 'pointer'
 }

 interface User {
  [key: string]: string; // Define an index signature
  email: string;
  password: string;
  first_name: string;
  middle_name: string;
  last_name: string;
  date_of_birth: string;
  state: string;
  city: string;
  street: string;
  profile_image: string;
  gender: string;
  zip_code: string;
}


 /**
  * signIn - function for regitering the form
  * @param e: Event
  * @returns boolean: true done, false failed
  */
  const signIn = (e: any) :boolean => {
     e.preventDefault()
     setLoginState({...loginState,showLoader:true,error:false})
     let i: any
     let user: User = loginState.inputData
      for (i in loginState.inputData)
        {
           if ( user.hasOwnProperty(i) && user[i] === "")
            {
              setLoginState({
                ...loginState,
                error:true,
                info: i.replaceAll("_", " ") + " is required",
                showLoader:false
              })
              return false
            }
        }

         makeRequest("users/register", loginState.inputData, (err, data)=>{

            if (err)
              {  
                
                setTimeout(()=>{
                  setLoginState({...loginState,showLoader:false,error:true,info:err.error})
                },3000)
                return
              }

              if (data['error'] !== null )
                {
                  
                  setTimeout(()=>{
                    setLoginState({...loginState,showLoader:false,error:true,info:data.error})
                  },3000)
                  return
                }


    
              setTimeout(()=>{
                setLoginState({...loginState,showLoader:false,error:false,info:"Registration successful",suc:true})
              },3000)


              setTimeout(()=>{
                router.push("/login")
              },3000)
    
 
          
       }).catch(error=>{
        setLoginState({...loginState,showLoader:false,error:true,info:error.message})
       })

       return true
  }
 

  const handleFileChange = async(e:any) => {

    e.preventDefault();
    const file = e.target.files[0];
 
    let form  = new FormData()

    form.append("profile_image", file)
  
    makeRequest("users/upload",form, (err, data)=>{

        if (err)
         { 
           return setLoginState({...loginState,showLoader:true,error:true, info: err.error})
         } 

         console.log(err, data)

         if (data['error'] !== null )
          {
            setTimeout(()=>{
              setLoginState({...loginState,showLoader:false,error:true,info:data.error})
            },3000)
            return false
          }
         
          let data_:any = {}
          let img = data.data.output_path_relative.replace("\\", "/")
          console.log(img)

          data_ = {...loginState, inputData:{...loginState.inputData, profile_image: img}}
          setLoginState(data_)
  
      

     }, "POST", {'Content-Type': 'multipart/form-data'}).catch(error=>{
      setLoginState({...loginState,showLoader:true,error:true, info: error.message})
     })
     
     return true
  };


 const getInput = (e:any)=>{
  e.preventDefault()
  let data:any = {}
  data = {...loginState, inputData:{...loginState.inputData, [e.target.name]: e.target.value }}
  setLoginState(data)
 }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between  text-white">

    <div className="flex min-h-full flex-1 w-full flex-col justify-center px-6 py-0 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm relative">
        <img
          className="mx-auto h-20 w-20"
          src="./images/logo.png"
          alt="Your Company"
        />
        
         {loginState.inputData.profile_image && (<img className="mx-auto h-20 w-20 rounded-full object-cover" src={backend_path+'/'+loginState.inputData.profile_image } alt="user profile pix"/>)}

        <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-white">
          Register
        </h2>

       

       {(loginState.error|| loginState.suc)  && <div role="alert" className={loginState.error?'alert alert-error':'alert alert-success'}>
        <svg onClick={()=>setLoginState({...loginState, error:false,suc:false})} xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <span>{loginState.info}</span>
      </div>}
     
                                                                                                              
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form className="space-y-6" action="#" method="POST" style={form_style} >
        <div>
            <label htmlFor="email" className="block text-sm font-medium leading-6 text-white">
              First name
            </label>
            <div className="mt-2">
              <input
                id="fname"
                name="first_name"
                type="text"
                autoComplete="none"
                onInput={(e)=>getInput(e)}
                required
                className="block w-full rounded-md border-0  
			   py-1.5 px-2 text-blue-600 shadow-sm 
			   ring-1 ring-inset ring-gray-300 
			   placeholder:text-gray-400 focus:ring-2
			   focus:ring-inset focus:ring-indigo-600 
		           sm:text-sm sm:leading-6"
              />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium leading-6 text-white">
              Middle name
            </label>
            <div className="mt-2">
              <input
                id="mname"
                name="middle_name"
                type="text"
                autoComplete="none"
                onInput={(e)=>getInput(e)}
                required
                className="block w-full rounded-md border-0 py-1.5 px-2 text-blue-600 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium leading-6 text-white">
              Last name
            </label>
            <div className="mt-2">
              <input
                id="lname"
                name="last_name"
                type="text"
                autoComplete="email"
                onInput={(e)=>getInput(e)}
                required
                className="block w-full rounded-md border-0 py-1.5 px-2 text-blue-600 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
            </div>
          </div>

          

          

          <div>
            <label htmlFor="email" className="block text-sm font-medium leading-6 text-white">
              Email address
            </label>
            <div className="mt-2">
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                onInput={(e)=>getInput(e)}
                required
                className="block w-full rounded-md border-0 py-1.5 px-2 text-blue-600 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
            </div>
          </div>
          
          <div>
            <div className="flex items-center justify-between">
              <label htmlFor="password" className="block text-sm font-medium leading-6 text-white">
                Password
              </label>
            
            </div>
            <div className="mt-2 relative">
              <input
                id="password"
                name="password"
                type= {loginState.showPassword? "text" : "password"}
                onInput={(e)=>getInput(e)}
                autoComplete="current-password"
                required
                className="block w-full rounded-md border-0 py-1.5 px-2 text-blue-600 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
              <span className="absolute" style={show_password_style} 
              onClick={()=>setLoginState({...loginState, showPassword: !loginState.showPassword})} >show</span>
            </div>
          </div>
           

          <div>
            <label htmlFor="email" className="block text-sm font-medium leading-6 text-white">
             Date of birth
            </label>
            <div className="mt-2">
              <input id="dob"
                name="date_of_birth"
                type="date"
                autoComplete="false"
                onInput={(e)=>getInput(e)}
                required
                className="block w-full rounded-md border-0 py-1.5 px-2 text-blue-600 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
            </div>
          </div>


          <div>
            <label htmlFor="email" className="block text-sm font-medium leading-6 text-white">
             State
            </label>
            <div className="mt-2">
              <input
                id="state"
                name="state"
                type="text"
                autoComplete="on"
                onInput={(e)=>getInput(e)}
                required
                className="block w-full rounded-md border-0 py-1.5 px-2 text-blue-600 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
            </div>
          </div>


          <div>
            <label htmlFor="email" className="block text-sm font-medium leading-6 text-white">
             City
            </label>
            <div className="mt-2">
              <input
                id="city"
                name="city"
                type="text"
                autoComplete="on"
                onInput={(e)=>getInput(e)}
                required
                className="block w-full rounded-md border-0 py-1.5 px-2 text-blue-600 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium leading-6 text-white">
             Street
            </label>
            <div className="mt-2">
              <input
                id="street"
                name="street"
                type="text"
                autoComplete="on"
                onInput={(e)=>getInput(e)}
                required
                className="block w-full rounded-md border-0 py-1.5 px-2 text-blue-600 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
            </div>
          </div>




         
        
          <div>
            <label htmlFor="email" className="block text-sm font-medium leading-6 text-white">
              Last name
            </label>
            <div className="mt-2">
            <select defaultValue={"Male"} name="gender" onInput={(e)=>getInput(e)}
             className="select select-primary w-full max-w-xs">
              <option disabled defaultValue={"Gender"}>Gender</option>
              <option>Male</option>
              <option>Female</option>
            </select>
            </div>
          </div> 
        
        <label className="form-control w-full max-w-xs">
        <div className="label">
          {/* <span className="label-text">Pick a file</span>
          <span className="label-text-alt">Alt label</span> */}
        </div>
        <input type="file" id="profile_pix_name" onInput={handleFileChange} name="profile_image" className="file-input file-input-bordered w-full max-w-xs" />
        <div className="label">
        
        </div>
      </label>
           
          <div>
          <Button name="Sign in"  onclick={signIn} styles_button={{background: "rgb(79 70 229/.4)",
            height:"28px", fontWeight: 500, position: 'relative', ...disble_button, minWidth:"100%"} } >
              <span className="loading loading-spinner loading-sm"  style = {{...spinner_style, position: "relative", display: loginState.showLoader?"block":"none"}}></span>
            </Button> 
          </div>
        </form>
        <p className="mt-10 text-center text-sm text-gray-500">
          Already a member?{' '}
          <Link href="/login" className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">
           Login
          </Link>
        </p>
      
      </div>
    </div>
    
    
  </main>
  )
}

export default Register
