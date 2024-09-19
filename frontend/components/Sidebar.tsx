import { useState, useEffect } from 'react';
import { FaTachometerAlt, FaProductHunt, FaChartLine, FaMoneyCheckAlt, FaSignOutAlt } from 'react-icons/fa';
import styles from './Sidebar.module.css';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { makeRequest } from '@/request';
import { useRouter } from 'next/navigation';

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter()
  const [hasLogout, setHasLogout] = useState<object | null>(null)
  // Get initial state from localStorage or fallback to default values
  const getInitialOpenMenu = () => localStorage.getItem('openMenu') || 'Dashboard';
  const getInitialActiveMenuItem = () => localStorage.getItem('activeMenuItem') || pathname;


  const [openMenu, setOpenMenu] = useState<string | null>(getInitialOpenMenu);
  const [activeMenuItem, setActiveMenuItem] = useState<string>(getInitialActiveMenuItem);

  // Sync the active menu item with the current pathname on page load
  useEffect(() => {
    setActiveMenuItem(pathname);
  }, [pathname]);

  // Persist the openMenu and activeMenuItem to localStorage
  useEffect(() => {
    localStorage.setItem('openMenu', openMenu || '');
  }, [openMenu]);

  useEffect(() => {
    localStorage.setItem('activeMenuItem', activeMenuItem);
  }, [activeMenuItem]);

  const sidebar = [
    {
      ele: 'ul',
      text: 'Dashboard',
      icon: <FaTachometerAlt className={styles.icon} />,
      children: [
        {
          ele: 'li',
          text: 'Dashboard Home',
          link: '/dashboard'
        }
      ]
    },

    {
      ele: 'ul',
      text: 'Product',
      icon: <FaProductHunt className={styles.icon} />,
      children: [
        {
          ele: 'li',
          text: 'Add product',
          link: '/add-product'
        },
        {
          ele: 'li',
          text: 'List product',
          link: '/list-product'
        },
       
      ]
    },
    {
      ele: 'ul',
      text: 'Expendicture',
      icon: <FaMoneyCheckAlt className={styles.icon} />,
      children: [
        {
          ele: 'li',
          text: 'Add expenditure',
          link: '/add-expenditure'
        },
        {
          ele: 'li',
          text: 'List Expenditure',
          link: '/list-expenditure'
        },
        
      ]
    },
    {
      ele: 'ul',
      text: 'Revenue',
      icon: <FaChartLine className={styles.icon} />,
      children: [
        {
          ele: 'li',
          text: 'Add Revenue',
          link: '/add-revenue'
        },
        {
          ele: 'li',
          text: 'list Revenue',
          link: '/list-revenue'
        }
      ]
    }
  ];

  const toggleMenu = (menu: string) => {
    setOpenMenu(openMenu === menu ? null : menu); // Toggle open/close
  };

  const handleMenuItemClick = (menuItem: string) => {
    setActiveMenuItem(menuItem);
  };

 const logout = async() => {
   const callback =  (err,data)=>{
    if (err) return setHasLogout(err)
    setHasLogout(data)
   return setTimeout(()=>{
            
      router.push('/login')
    },3000)

   }

   await  makeRequest('users/logout', {},callback, 'POST') 
 } 
  return (
    <div className={styles.sidebar} style={{position:"relative"}}>
      
      {( hasLogout && (hasLogout.error|| hasLogout.success))  && <div role="alert" className={hasLogout.error?'alert alert-error':'alert alert-success'} style={{position:"absolute", zIndex:"2"}}>
          <svg onClick={()=>setHasLogout({...hasLogout, error:false,suc:false})} xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span>{hasLogout.message}</span>
        </div>}
      
      {sidebar.map((ele, ind) => (
        <ul key={ind} className={styles.menu}>
          <span
            className={styles.sectionTitle}
            onClick={() => toggleMenu(ele.text)}
          >
            {ele.icon}
            {ele.text}
          </span>
          {ele.children.map((chele, index) => (
            <Link href={chele.link} key={index} id={styles.content}>
              <li
                key={index}
                className={`${styles.menuItem}
                  ${openMenu === ele.text ? styles['slide-down'] : styles['slide-up']} 
                  ${activeMenuItem === chele.link ? styles.active : ''}
                `}
                onClick={() => handleMenuItemClick(chele.link)}
              >
                {chele.text}
              </li>
            </Link>
          ))}
        </ul>
      ))}

      <div className="flex items-center cursor-pointer" onClick={logout}>
        <FaSignOutAlt className="mr-2" />
        <div>Logout</div>
      </div>
    </div>
  );
}
