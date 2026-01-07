import React, { useState } from 'react';
import './Directory.css';

const STAFF_DATA = [
    { name: "Maria", title: "General Administrator", phone: "(203)-460-4309", category: "Admin", focus: "General Support" },
    { name: "Aimme", title: "Office Manager", phone: "(475)-370-3682 ext 103", category: "Admin", focus: "Billing, Payments, Dumpster Production" },
    { name: "Alex (Office)", title: "Production Assistant", phone: "(475)-370-3672 ext 105", category: "Admin", focus: "Permits, Building Dept, Field Crew Calls" },
    { name: "Jolie", title: "Marketing Director", phone: "(475)-370-3691 ext 104", category: "Admin", focus: "Marketing, Advertising, Partnerships" },
    { name: "Jonah", title: "Data Analyst", phone: "(203)-446-3121 ext 102", category: "Admin", focus: "Business Data, Lead Calling" },
    { name: "Francisco", title: "Logistics Manager", phone: "(475)-289-4256", category: "Admin", focus: "Dumpster Pick-up & Delivery" },
    { name: "Michael", title: "Insurance Specialist", phone: "(203)-525-9944", category: "Sales", focus: "Insurance Claims, Roofing, Siding" },
    { name: "Evan", title: "Field Expert", phone: "(203)-917-7133", category: "Sales", focus: "Roofing, Decks (NY, RI, NH)" },
    { name: "Ray", title: "Field Expert", phone: "(203)-290-1847", category: "Sales", focus: "Roofing, Siding (NY Focus)" },
    { name: "Luis", title: "Commercial Lead", phone: "(203)-942-9088", category: "Sales", focus: "Metal/Cedar/Slate, Commercial" },
    { name: "Alex (Field)", title: "Field Expert", phone: "(203)-837-0356", category: "Sales", focus: "Roofing, Gutters, Skylights" },
    { name: "Jorge", title: "Remodel Specialist", phone: "(203)-617-5484", category: "Sales", focus: "Interior Remodels, Kitchens, Bathrooms" },
    { name: "Agustin", title: "Project Manager", phone: "(203)-917-1228", category: "Production", focus: "Siding Repairs (Required Photos first)" },
    { name: "Jeremy", title: "Roofing PM", phone: "(475)-455-0774", category: "Production", focus: "Roofing Project Management" },
    { name: "Marcelo", title: "Fabrication Lead", phone: "(203)-984-8591", category: "Production", focus: "Metal Fabrication & Takeoffs" }
];

function Directory() {
    const [search, setSearch] = useState("");

    const filteredStaff = STAFF_DATA.filter(staff =>
        staff.name.toLowerCase().includes(search.toLowerCase()) ||
        staff.title.toLowerCase().includes(search.toLowerCase()) ||
        staff.focus.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="directory-container">
            <div className="directory-header">
                <h2>Company Directory</h2>
                <div className="search-bar">
                    <input
                        type="text"
                        placeholder="Search by name, role, or focus..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                </div>
            </div>

            <div className="directory-grid">
                {filteredStaff.map((staff, idx) => (
                    <div key={idx} className="staff-card">
                        <div className="staff-category" data-cat={staff.category}>{staff.category}</div>
                        <div className="staff-main">
                            <h3 className="staff-name">{staff.name}</h3>
                            <div className="staff-title">{staff.title}</div>
                        </div>
                        <div className="staff-details">
                            <div className="detail-item">
                                <span className="icon">📞</span>
                                <a href={`tel:${staff.phone}`}>{staff.phone}</a>
                            </div>
                            <div className="detail-focus">
                                <strong>Focus:</strong> {staff.focus}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {filteredStaff.length === 0 && (
                <div className="no-results">No staff members found matching "{search}"</div>
            )}
        </div>
    );
}

export default Directory;
