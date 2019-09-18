//
//  XCUIApplication.swift
//  MobiliumDriver
//
//  Created by Mateusz Mularski on 12/09/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import XCTest

extension XCUIApplication {
    func element(with accessibilityId: String) -> XCUIElement {
        return descendants(matching: .any)[accessibilityId].firstMatch
    }

    func performIfElementExists(with accessibilityId: String, action: (XCUIElement) -> Void) -> Bool {
        let element = self.element(with: accessibilityId)
        guard element.exists else { return false }
        
        action(element)
        return true
    }
}
