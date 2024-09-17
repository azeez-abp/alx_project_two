import { useState, useEffect } from 'react';
import { FaTachometerAlt, FaProductHunt, FaChartLine, FaMoneyCheckAlt } from 'react-icons/fa';
import styles from './Sidebar.module.css';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Sidebar() {
  const pathname = usePathname();

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

  return (
    <div className={styles.sidebar}>
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
    </div>
  );
}
