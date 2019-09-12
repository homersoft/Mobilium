//
//  XCUIApplication.swift
//  MobiliumDriver
//
//  Created by Mateusz Mularski on 12/09/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import XCTest

extension XCUIApplication {
    private var hideKeyboardButton: XCUIElement {
        return keyboards.buttons["Hide keyboard"]
    }
    
    private var dismissKeyboardButton: XCUIElement {
        return keyboards.buttons["Dismiss"]
    }
    
    func element(with accessibilityID: String) -> XCUIElement {
        return descendants(matching: .any)[accessibilityID]
    }
    
    func hideKeyboard() {
        if hideKeyboardButton.exists {
            hideKeyboardButton.tap()
        } else if dismissKeyboardButton.exists {
            dismissKeyboardButton.tap()
        }
    }
}
