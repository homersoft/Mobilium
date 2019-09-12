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
        return descendants(matching: .any)[accessibilityID]
    }
    
    func hideKeyboard() {
        if keyboards.buttons["Hide keyboard"].exists {
            keyboards.buttons["Hide keyboard"].tap()
        } else if keyboards.buttons["Dismiss"].exists {
            keyboards.buttons["Dismiss"].tap()
        }
    }
}
