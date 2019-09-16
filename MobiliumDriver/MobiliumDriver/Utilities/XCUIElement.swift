//
//  XCUIElement.swift
//  MobiliumDriver
//
//  Created by Mateusz Mularski on 13/09/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import XCTest

// MARK: buttons
extension XCUIElement {
    var hideKeyboardButton: XCUIElement {
        return keyboards.buttons["Hide keyboard"]
    }
    
    var dismissKeyboardButton: XCUIElement {
        return keyboards.buttons["Dismiss"]
    }
}

// MARK: mutating methods
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
}
