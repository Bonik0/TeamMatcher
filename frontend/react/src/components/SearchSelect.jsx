import React, { useEffect, useRef, useState } from "react";
import { defaultStyles } from "../styles/default";
import { searchSelectStyles } from "../styles/searchSelect";

export default function SearchSelect({
	placeholder,
	fetchUrl,
	onSelect,
	executedName,
	selectedItems,
	saveSelected = false,
	onInputChange,
	inputStyle,
}) {
	const LIMIT = 100;
	const OFFSET = 0;
	const [input, setInput] = useState("");
	const [suggestions, setSuggestions] = useState([]);
	const [open, setOpen] = useState(false);
	const timeoutRef = useRef(null);
	const containerRef = useRef(null);

	useEffect(() => {
		const onClick = (e) => {
			if (containerRef.current && !containerRef.current.contains(e.target)) {
				setOpen(false);
			}
		};
		document.addEventListener("mousedown", onClick);
		return () => document.removeEventListener("mousedown", onClick);
	}, []);

	useEffect(() => {
		if (timeoutRef.current) {
			clearTimeout(timeoutRef.current);
		}

		timeoutRef.current = setTimeout(async () => {
			try {
				const params = new URLSearchParams({
					q: input,
					limit: LIMIT,
					offset: OFFSET,
				});

				const response = await fetch(
					`http://localhost:8000${fetchUrl}?${params.toString()}`,
				);
				if (!response.ok) {
					setSuggestions([]);
					return;
				}
				const response_dict = await response.json();
				const existing = selectedItems || [];
				const filtered = response_dict[executedName].filter(
					(it) =>
						!existing.some((sel) =>
							String(sel.id) === String(it.id) || sel.name === it.name
						),
				);
				setSuggestions(filtered);
			} catch (error) {
				setSuggestions([]);
			}
		}, 250);

		return () => {
			if (timeoutRef.current) {
				clearTimeout(timeoutRef.current);
			}
		};
	}, [input, fetchUrl, executedName, selectedItems?.length]);

	const handleSelect = (item) => {
		const inputValue = (saveSelected === true) ? item.name : "";
		onSelect(item);
		setInput(inputValue);
		setSuggestions([]);
		setOpen(false);
	};

	return (
		<div style={searchSelectStyles.container} ref={containerRef}>
			<input
				type="text"
				placeholder={placeholder}
				value={input}
				onChange={(e) => {
					const value = e.target.value;
					setInput(value);
					if (typeof onInputChange === "function") {
						onInputChange(value);
					}
				}}
				style={{ ...defaultStyles.input, ...(inputStyle || {}) }}
				onBlur={() => {
					if (saveSelected && input && input.trim()) {
						onSelect({ name: input.trim() });
					}
				}}
				onFocus={() => {
					if (suggestions.length) {
						setOpen(true);
					}
				}}
			/>

			{open && suggestions && suggestions.length > 0 && (
				<ul style={searchSelectStyles.dropdown}>
					{suggestions.map((s, i) => {
						return (
							<li
								key={i}
								onClick={() => handleSelect(s)}
								style={searchSelectStyles.dropdownItem}
								onMouseEnter={(e) => {
									e.currentTarget.style.background =
										searchSelectStyles.itemHoverBg;
								}}
								onMouseLeave={(e) => {
									e.currentTarget.style.background = "transparent";
								}}
							>
								{s.name}
							</li>
						);
					})}
				</ul>
			)}
		</div>
	);
}
