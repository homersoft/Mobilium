//
//  XCUIApplication.swift
//  MobiliumDriver
//
//  Created by Mateusz Mularski on 12/09/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import XCTest

extension XCUIApplication {
    func element(with accessibilityID: String) -> XCUIElement {
        return descendants(matching: .any)[accessibilityID].firstMatch
    }
    
    func hideKeyboard() {
        if hideKeyboardButton.exists {
            hideKeyboardButton.tap()
        } else if dismissKeyboardButton.exists {
            dismissKeyboardButton.tap()
        }
    }
}
