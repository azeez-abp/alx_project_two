'use client'
/*import Image from "next/image";*/
import Link from 'next/link'

export default function Home(): any {

  return (
    <main className="flex min-h-screen flex-col items-center justify-between py-0 text-white">
     
       <div className='header flex w-full'>
       <div className="flex-1 w-20">
          My Farm Insight
        </div>

        <div className="flex-1 w-80">
           <Link href={"/login"} className='mx-5'>Login</Link>
           <Link href={"/register"} className='mx-5'>Register</Link>
        </div>

        <div className="flex-1 w-20">
          The solution that improve farm performance
        </div>
       </div>
         
         <div>
            <h1 style={{fontSize:'60px'}}> FARM PROJECT</h1>
         </div>

       <div className='body flex min-h-screen flex-col w-full' style={{backgroundImage: 'url("./images/farm.jpg")', backgroundSize:"cover", backgroundRepeat:'no-repeat'}}>
             
             
             <div className='flex justify-center h-screen content-center flex-wrap p-5'> 


                <div className="flex-1 w-50 text-left">

                    <h1 style={{fontSize:'30px'}}>My Farm Insight</h1> 
                    <div style={{width: '50%'}} className='text-start'>Monitor the activity on farm, Know the chemistry of  drug administered to farm animals
                      </div>
                </div>


                <div className="flex-1 w-50 text-left">
                <h1 style={{fontSize:'30px'}}>Improve Farm Performance</h1> 
                <div style={{ width: '50%'}} className='text-start'>Increase sale and generate more revenue for your farm
                      </div>
                </div>
 

            </div>

       </div>
       <div className='footer'>

         <div className="about p-10">
            <h1 style={{fontSize:'20px'}}> About</h1>
             <div>
              The project is a solution that enables farm owners <br/>
              to monitor workers activities on the farm.<br/>
              This will able the owner to know the quatitative values of drug<br/>
              administered to the life stocks on the farm.
            
             </div>
         </div>

         <div className="about p-10">
            <h1 style={{fontSize:'20px'}}> Team</h1>
             <div>
              <ul>
                <li><Link href={'https://github.com/azeez-abp/'}>Azeez adio</Link> </li>
              </ul>
             </div>
         </div>
       </div>
         
    </main>
  );
}
