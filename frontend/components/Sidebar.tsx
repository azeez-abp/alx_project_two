import { useState } from 'react';
import { FaTachometerAlt, FaProductHunt, FaMoneyCheckAlt, FaChartLine } from 'react-icons/fa';
import styles from './Sidebar.module.css';
import Link  from 'next/link'

export default function Sidebar() {
  const [openMenu, setOpenMenu] = useState('dashboard'); // Set 'dashboard' open by default
  const [activeMenuItem, setActiveMenuItem] = useState('dashboard'); // Set 'dashboard' active by default

  const toggleMenu = (menu:any) => {
    setOpenMenu(openMenu === menu ? null : menu);
  };

  const handleMenuItemClick = (menuItem:any) => {
    setActiveMenuItem(menuItem);
  };
  console.log(styles)

  return (

    <div className={styles.sidebar}>
      <ul className={styles.menu} >
       
        <span className={styles.sectionTitle} onClick={() => toggleMenu('dashboard')}>
          <FaTachometerAlt className={styles.icon} /> Dashboard
        </span>
        <Link href={'/dashboard'}   id={styles.content} className={` ${openMenu === 'dashboard' ? styles['slide-down'] : styles['slide-up']}`} >
            <li className={`${styles.menuItem} ${openMenu === 'dashboard' ? styles.show : ''} ${
                activeMenuItem === 'dashboard' ? styles.active : ''
            }`}
            onClick={() => handleMenuItemClick('dashboard')}
            >

            Dashboard Home
            </li>
            
        </Link>
      
      </ul>

      <ul className={styles.menu}>
        <span className={styles.sectionTitle} onClick={() => toggleMenu('product')}>
          <FaProductHunt className={styles.icon} /> Product
        </span>
        <Link href={'/add-product'}>
        <li
          className={`${styles.menuItem} ${openMenu === 'product' ? styles.show : ''} ${
            activeMenuItem === 'addProduct' ? styles.active : ''
          }`}
          onClick={() => handleMenuItemClick('addProduct')}
        >
          Add Product
        </li>
        </Link>
        <Link href={'/list-product'}>
        <li
          className={`${styles.menuItem} ${openMenu === 'product' ? styles.show : ''} ${
            activeMenuItem === 'listProduct' ? styles.active : ''
          }`}
          onClick={() => handleMenuItemClick('listProduct')}
        >
          List Product
        </li>
        </Link>
      </ul>

      <ul className={styles.menu}>
        <span className={styles.sectionTitle} onClick={() => toggleMenu('expenditure')}>
          <FaMoneyCheckAlt className={styles.icon} /> Expenditure
        </span>
        <li
          className={`${styles.menuItem} ${openMenu === 'expenditure' ? styles.show : ''} ${
            activeMenuItem === 'addExpenditure' ? styles.active : ''
          }`}
          onClick={() => handleMenuItemClick('addExpenditure')}
        >
          Add Expenditure
        </li>
        <li
          className={`${styles.menuItem} ${openMenu === 'expenditure' ? styles.show : ''} ${
            activeMenuItem === 'listExpenditure' ? styles.active : ''
          }`}
          onClick={() => handleMenuItemClick('listExpenditure')}
        >
          List Expenditure
        </li>
      </ul>

      <ul className={styles.menu}>
        <span className={styles.sectionTitle} onClick={() => toggleMenu('revenue')}>
          <FaChartLine className={styles.icon} /> Revenue
        </span>
        <li
          className={`${styles.menuItem} ${openMenu === 'revenue' ? styles.show : ''} ${
            activeMenuItem === 'addRevenue' ? styles.active : ''
          }`}
          onClick={() => handleMenuItemClick('addRevenue')}
        >
          Add Revenue
        </li>
        <li
          className={`${styles.menuItem} ${openMenu === 'revenue' ? styles.show : ''} ${
            activeMenuItem === 'listRevenue' ? styles.active : ''
          }`}
          onClick={() => handleMenuItemClick('listRevenue')}
        >
          List Revenue
        </li>
      </ul>
    </div>
  );
}
