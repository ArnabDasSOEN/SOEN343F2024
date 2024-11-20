import { Link } from "react-router-dom";
import { DashboardCard } from "../Components/DashboardCard/DashboardCard";
import './CSS/UserHomePage.css'

export const UserHomePage = () => {
    return(
        <div className="user-homepage">
            <h1>Welcome to your User Dashboard</h1>
            <div className="user-homepage-cards-container">
                
                <Link to="/dashboard" className="requestdelivery"><DashboardCard title = "Request Delivery" description = "Start a new delivery request here"/></Link>
                

                <Link to="/trackOrders"><DashboardCard title = "Track Delivery" description = "View the status of ongoing delivieries here"/></Link>


                <Link to="/viewOrders"><DashboardCard title = "View Orders" description = "View your orders you've already payed for"/></Link>


                <Link to="/viewDeliveryRequest"><DashboardCard title = "View Delivery Requests" description = "View your pending delivery requests"/></Link>

                <Link to="/cancelDeliveryRequest"><DashboardCard title = "Cancel Delivery Requests" description = "Cancel your delivery requests here"/></Link>

                <Link to="/payDeliveryRequest"><DashboardCard title = "Pay Delivery Requests" description = "Pay for a delivery requests you already made"/></Link>

            </div>
        </div>
    );

}