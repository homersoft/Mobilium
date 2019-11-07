//
//  XPathParserTests.swift
//  MobiliumDriverTests
//
//  Created by Tomasz Oraczewski on 06/11/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

@testable import MobiliumFramework
import XCTest

class XPathParserTests: XCTestCase {

    func testParseEmptyXPath() {
        let result = XPathParser.parse("")

        XCTAssertTrue(result.isEmpty)
    }

    func testParseCell() {
        let result = XPathParser.parse("//XCUIElementTypeCell")

        let expected = [Path(elementType: .cell)]
        XCTAssertEqual(result, expected)
    }

    func testParseButton() {
        let result = XPathParser.parse("//XCUIElementTypeButton")

        let expected = [Path(elementType: .button)]
        XCTAssertEqual(result, expected)
    }

    func testParseNavigationBar() {
        let result = XPathParser.parse("//XCUIElementTypeNavigationBar")

        let expected = [Path(elementType: .navigationBar)]
        XCTAssertEqual(result, expected)
    }

    func testParseTextView() {
        let result = XPathParser.parse("//XCUIElementTypeTextView")

        let expected = [Path(elementType: .textView)]
        XCTAssertEqual(result, expected)
    }

    func testParseSwitchButton() {
        let result = XPathParser.parse("//XCUIElementTypeSwitch")

        let expected = [Path(elementType: .switchButton)]
        XCTAssertEqual(result, expected)
    }

    func testParseConditionWithLabelParameter() {
        let result = XPathParser.parse("//XCUIElementTypeButton[contains(@label, 'menu')]")

        XCTAssertEqual(result[0].condition?.parameterType, .label)
    }

    func testParseConditionWithValueParameter() {
        let result = XPathParser.parse("//XCUIElementTypeButton[contains(@value, 'menu')]")

        XCTAssertEqual(result[0].condition?.parameterType, .value)
    }

    func testParseMultipleElementsWithConditions() {
        let xpath = """
        //XCUIElementTypeCell[contains(@label, 'lala')]/XCUIElementTypeButton[contains(@value, 'remove_button')]
        """

        let result = XPathParser.parse(xpath)

        let expectedCondition = PathCondition(type: .contains, parameterType: .label, value: "lala")
        let expectedCondition2 = PathCondition(type: .contains, parameterType: .value, value: "remove_button")
        let expected = [Path(elementType: .cell, condition: expectedCondition),
                        Path(elementType: .button, condition: expectedCondition2)]
        XCTAssertEqual(result, expected)
    }

    func testParseMultipleElementsWithSingleCondition() {
        let xpath = "//XCUIElementTypeCell/XCUIElementTypeButton[contains(@value, 'remove_button')]"

        let result = XPathParser.parse(xpath)

        let expectedCondition = PathCondition(type: .contains, parameterType: .value, value: "remove_button")
        let expected = [Path(elementType: .cell),
                        Path(elementType: .button, condition: expectedCondition)]
        XCTAssertEqual(result, expected)
    }

    func testParseMultipleElementsWithoutConditions() {
        let xpath = "//XCUIElementTypeCell/XCUIElementTypeButton"

        let result = XPathParser.parse(xpath)

        let expected = [Path(elementType: .cell),
                        Path(elementType: .button)]
        XCTAssertEqual(result, expected)
    }
}
