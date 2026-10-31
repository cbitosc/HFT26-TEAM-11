
"use client";

import { useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  CircleMarker,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const sightings = [
  { name: "Indian Leopard", zone: "Western Ghats", lat: 15.3173, lng: 75.7139, confidence: 98.6, color: "#22c55e" },
  { name: "Bengal Tiger", zone: "Core Forest", lat: 15.42, lng: 75.82, confidence: 96.2, color: "#f97316" },
  { name: "Asian Elephant", zone: "Watering Point", lat: 15.25, lng: 75.91, confidence: 94.8, color: "#38bdf8" },
  { name: "Sloth Bear", zone: "Western Ghats", lat: 15.36, lng: 75.65, confidence: 91.4, color: "#c084fc" },
  { name: "Spotted Deer", zone: "Grassland", lat: 15.48, lng: 75.72, confidence: 89.7, color: "#facc15" },
  { name: "Indian Leopard", zone: "Core Forest", lat: 15.39, lng: 75.9, confidence: 97.1, color: "#22c55e" },
];

export default function WildlifeMap() {
  return (
    <div className="overflow-hidden rounded-2xl border border-emerald-900">
      <MapContainer
        center={[15.35, 75.78]}
        zoom={10}
        scrollWheelZoom={true}
        style={{ height: "550px", width: "100%" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {sightings.map((item, index) => (
          <CircleMarker
            key={index}
            center={[item.lat, item.lng]}
            radius={10}
            pathOptions={{
              color: item.color,
              fillColor: item.color,
              fillOpacity: 0.85,
            }}
          >
            <Popup>
              <strong>{item.name}</strong>
              <br />
              Zone: {item.zone}
              <br />
              Confidence: {item.confidence}%
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
