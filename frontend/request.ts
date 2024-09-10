

import axios from 'axios'
  export const backend_path  = "http://localhost:9393"
  axios.defaults.withCredentials = true; 
 
  export  const  makeRequest: (url: string, data: any, cb: (error?: object | null | any , response?: object | null | any) => void, mtd?: string, headers_opt?: any) => Promise<void> = async (url, data, cb, mtd, headers_opt) =>{
  let   header_setting  = headers_opt !==undefined ?headers_opt: { 
    //  'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Type': 'application/json',
      'authorization':  `Bearer ${localStorage.getItem("alx_token")}`,
     }
   
        const options = {
            method: mtd? mtd: 'POST',
            headers:header_setting,
            
            // body:  {userID:inp},
            //credentials: 'include',
            data:  data,
            url:`${backend_path}/api/v1/${url}`
          };
          try {
         //   console.log(app_domain_proxy+ url)
             let d  =  await axios(options)
             let out  = d.data
            //  console.log("TYR", out, d)
            
              if(out.error === true){
                return cb(out, null)
               }
                
 
               return cb(null,out)  
    
    
          } catch (error:any) {
              //  console.log(error)
             if (
             error &&
             error.hasOwnProperty('response') && 
             error.response.hasOwnProperty('data') && 
             error.response.data.hasOwnProperty('error')) 
             {
               return cb(error.response.data,null)// Property exists, safe to use error.response.dat
             }
            
            return cb({error: error.message},null)
           
          }
    
    
        }
            
