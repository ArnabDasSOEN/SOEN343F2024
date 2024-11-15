import { Link } from "react-router-dom";
import { useState } from "react";
import axios from "axios";

export const Dashboard = () => {

    //how the data should look
    // "customer_id": "{{customerId}}",
    // "pick_up_address": {
    //     "street": "123 Main St",
    //     "house_number": "123",
    //     "apartment_number": "2B",
    //     "postal_code": "12345",
    //     "city": "New York",
    //     "country": "USA"
    // },
    // "drop_off_address": {
    //     "street": "456 Elm St",
    //     "house_number": "456",
    //     "apartment_number": "4A",
    //     "postal_code": "67890",
    //     "city": "Los Angeles",
    //     "country": "USA"
    // },
    // "package": {
    //     "unit_system": "imperial",
    //     "width_in": 10,
    //     "length_in": 20,
    //     "height_in": 5,
    //     "weight_lb": 30,
    //     "is_fragile": true,
    //     "package_items": [
    //         {
    //             "item_description": "Glass Vase",
    //             "quantity": 2,
    //             "weight": 1.5
    //         },
    //         {
    //             "item_description": "Fragile Sculpture",
    //             "quantity": 1,
    //             "weight": 2.0
    //         }
    //     ]
    // },









    const handleSubmitForm = (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);
        const formObject = Object.fromEntries(formData.entries()); //data to send to axios post requst to "/create_delivery_request"
    }

    const [pickUpAddress, setPickUpAddress] = useState({
        street: "",
        houseNumber: "",
        apartmentNumber: "",
        postalCode: "",
        city: "",
        country: ""
    });

    const handlePickUpAddressChange = (e) => {
        const { name, value } = e.target;
        //using the queue syntax so that we can use the most up to date/relevant data that we need
        //scatter the previous elements of the object, and just update the new one. This event only gets triggered for when an input changes. This means the target will always be that specific input element that changes.
        //hence, it will always have a name and a value (the name tag we specify and the value it contains)
        setPickUpAddress((prev) => ({ ...prev, [name]: value }),
    );
        
    }

    const [dropOffAddress, setDropOffAddress] = useState({
        street: "",
        houseNumber: "",
        apartmentNumber: "",
        postalCode: "",
        city: "",
        country: ""
    });
    //nott sure
    const handleDropOffChange = (e) => {
        const { name, value } = e.target;
        setDropOffAddress((prev) => ({ ...prev, [name]: value }));
    };


    //code for imperial units change.
    const [selectedUnit, setSelectedUnit] = useState("imperial units");
    const handleChangeUnits = (e) => {
        setSelectedUnit(e.target.value);
    }

    const [packageInfo, setPackageInfo] = useState({
        unitSystem: selectedUnit,
        length: "",
        width: "",
        height: "",
        weight: "",
        isFragile: ""
    });
    //not sure
    const handlePackageChange = (e) => {
        const { name, value } = e.target;
        setPackageInfo((prev) => ({ ...prev, [name]: value }));
        console.log(packageInfo.isFragile);
    };





    return (
        <main className="Dashboard">
            <h1>Dashboard</h1>
            <h2>make request for delivery</h2>

            <form action="/create_delivery_request" method="POST" onSubmit={handleSubmitForm}>

                <h3>pick up location</h3>
                <label>
                    street:
                    <input type="text" name="street" value={pickUpAddress.street} onChange={handlePickUpAddressChange} ></input>
                </label>

                <label>
                    house number:
                    <input type="number" name="street" value={pickUpAddress.houseNumber} onChange={handlePickUpAddressChange} ></input>
                </label>

                <label>
                    appartment number (if applies):
                    <input type="number" name="street" value={pickUpAddress.apartmentNumber} onChange={handlePickUpAddressChange} ></input>
                </label>

                <label>
                    POSTAL CODE:
                    <input type="text" name="street" value={pickUpAddress.postalCode} onChange={handlePickUpAddressChange}></input>
                </label>

                <label>
                    Country:
                    <input type="text" name="street" value={pickUpAddress.country} onChange={handlePickUpAddressChange}></input>
                </label>




                <h3>pick up location</h3>
                <label>
                    street:
                    <input type="text" name="street" value={dropOffAddress.street} onChange={handleDropOffChange} ></input>
                </label>

                <label>
                    house number:
                    <input type="number" name="street" value={dropOffAddress.houseNumber} onChange={handleDropOffChange}></input>
                </label>

                <label>
                    appartment number (if applies):
                    <input type="number" name="street" value={dropOffAddress.apartmentNumber} onChange={handleDropOffChange}></input>
                </label>

                <label>
                    POSTAL CODE:
                    <input type="text" name="street" value={dropOffAddress.postalCode} onChange={handleDropOffChange}></input>
                </label>

                <label>
                    Country:
                    <input type="text" name="street" value={dropOffAddress.country} onChange={handleDropOffChange}></input>
                </label>



                <h3>Package information</h3>
                <select value={selectedUnit} onChange={handleChangeUnits}>
                    <option value="imperial units">imperial units (freedom units - inches and lbs)</option>
                    <option value="metric units">metric units (non stupid units - cm and kg)</option>
                </select>
                <div>
                    {selectedUnit === 'imperial units' ? (
                        <p>You have chosen <b>Imperial units</b>. Measurements are in <b>inches</b> and <b>pounds</b>.</p>
                    ) : (
                        <p>You have chosen <b>Metric units</b>. Measurements are in <b>centimeters</b> and <b>kilograms</b>.</p>
                    )}
                </div>


                <label>
                    length:
                    <input type="number" name="length" value={packageInfo.length} onChange={handlePackageChange}></input>
                </label>
                <label>
                    width:
                    <input type="number" name="width" value={packageInfo.width} onChange={handlePackageChange}></input>
                </label>
                <label>
                    height:
                    <input type="number" name="height" value={packageInfo.height} onChange={handlePackageChange}></input>
                </label>
                <label>
                    weight:
                    <input type="number" name="weight" value={packageInfo.weight} onChange={handlePackageChange}></input>
                </label>

                <h3>Is this item fragile?</h3>
                <label>
                    yes
                    <input type="radio" name="isFragile" value={true} checked={packageInfo.isFragile === true} onChange={handlePackageChange} />
                </label>
                <label>
                    no
                    <input type="radio" name="isFragile" value={false} checked={packageInfo.isFragile === false} onChange={handlePackageChange}/>
                </label>
                <button type="submit">submit delivery request</button>
            </form>




            <Link to="/logout" className="logout">logout</Link>
        </main>
    )
}