//
//  XCUIElement.swift
//  MobiliumDriver
//
//  Created by Mateusz Mularski on 13/09/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import XCTest

extension XCUIElement {
    func clearText() {
        guard let text = value as? String else { return }
        
        let clearString = String(repeating: XCUIKeyboardKey.delete.rawValue, count: text.count)
        typeText(clearString)
    }
    
    func replaceText(with newText: String) {
        clearText()
        typeText(newText)
    }

    func setText(_ text: String, replace: Bool) {
        tap()
        if replace {
            replaceText(with: text)
        } else {
            typeText(text)
        }
    }

    func setSelectionOfCheckbox(to desirableSelectionState: Bool) -> Bool {
        guard let currentValue = value as? String else { return false }

        let isSelected = Int(currentValue) == 1
        if isSelected != desirableSelectionState {
            tap()
        }
        return true
    }
}
