//
//  LoginViewController.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/03/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import UIKit
import Combine

class LoginViewController: ViewController, UIPickerViewDelegate, UIPickerViewDataSource {
    private lazy var loginStackView = UIStackView.makeForAutolayout()
        .set(\.spacing, to: 20)
        .set(\.axis, to: .vertical)
    private lazy var phoneStackView = UIStackView.makeForAutolayout()
        .set(\.spacing, to: 20)
        .set(\.alignment, to: .leading)
        .set(\.distribution, to: .fill)

    private lazy var countryCodeTextField = UITextField()
        .set(\.text, to: "+48")
        .set(\.inputView, to: pickerView)
        .set(\.inputAccessoryView, to: pickerView.toolBar)
        .set(\.horizontalContentHuggingPriority, to: .defaultHigh)
    
    private lazy var phoneNumberTextField = UITextField()
        .set(\.keyboardType, to: .phonePad)
        .set(\.returnKeyType, to: .done)
        .set(\.placeholder, to: "Phone number")
        .set(\.accessibilityIdentifier, to: "phone_field")
    
    private lazy var verificationCodeTextField = UITextField()
        .set(\.returnKeyType, to: .done)
        .set(\.placeholder, to: "Verification code")
        .set(\.textContentType, to: .oneTimeCode)
        .set(\.accessibilityIdentifier, to: "code_field")

    private lazy var loginButton = UIButton.makeForAutolayout()
        .set(\.backgroundColor, to: .purple)
        .set(\.title, to: "Login")
        .set(\.accessibilityIdentifier, to: "login_button")
    
    private lazy var loadingIndicator = UIActivityIndicatorView.makeForAutolayout()
        .set(\.hidesWhenStopped, to: true)
        .set(\.accessibilityIdentifier, to: "loading_indicator")
    
    private lazy var pickerView = PickerView()
        .set(\.dataSource, to: self)
        .set(\.delegate, to: self)
        .set(\.onDone, to: { [weak phoneNumberTextField] in phoneNumberTextField?.becomeFirstResponder() })

    private var cancellables: Set<AnyCancellable> = []
    private var countryCodes: [String] = ["+48"]

    // MARK: - Lifecycle

    override func viewDidLoad() {
        super.viewDidLoad()
        title = "Login"
        initializeButtons()
    }

    override func initializeSubviews() {
        super.initializeSubviews()
        [loginButton, loginStackView, loadingIndicator].forEach(view.addSubview)
        initializeStackViews()
    }

    override func createConstraints() {
        super.createConstraints()
        let layoutGuide = view.safeAreaLayoutGuide
        NSLayoutConstraint.activate([
            loginStackView.centerYAnchor.constraint(equalTo: view.centerYAnchor),
            loginStackView.leadingAnchor.constraint(equalTo: layoutGuide.leadingAnchor, constant: 20),
            loginStackView.trailingAnchor.constraint(equalTo: layoutGuide.trailingAnchor, constant: -20),
            loginButton.topAnchor.constraint(equalTo: loginStackView.bottomAnchor, constant: 20),
            loginButton.leadingAnchor.constraint(equalTo: loginStackView.leadingAnchor),
            loginButton.trailingAnchor.constraint(equalTo: loginStackView.trailingAnchor),
            loadingIndicator.centerXAnchor.constraint(equalTo: layoutGuide.centerXAnchor),
            loadingIndicator.centerYAnchor.constraint(equalTo: layoutGuide.centerYAnchor)
        ])
    }
    
    private func initializeButtons() {
        loginButton.addTarget(self, action: #selector(login(_:)), for: .touchUpInside)
    }

    // MARK: - PickerViewDataSource

    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        countryCodes.count
    }

    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        1
    }

    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        "\(countryCodes[row])"
    }

    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        let country = countryCodes[row]
        countryCodeTextField.text = country
    }

    // MARK: - Private

    private func initializeStackViews() {
        [phoneStackView, verificationCodeTextField].forEach(loginStackView.addArrangedSubview)
        [countryCodeTextField, phoneNumberTextField].forEach(phoneStackView.addArrangedSubview)
    }

    @objc private func login(_ sender: Any?) {
        guard let phone = phoneNumberTextField.text, let code = verificationCodeTextField.text else { return }
        if phone.isEmpty || code.isEmpty {
            showAlert(with: "Ops", message: "Please provide input data")
        } else {
            showAccountView()
        }
    }
    
    private func showAccountView() {
        let vc = ModuleFactory().makeAccountVC()
        navigationController?.setViewControllers([vc], animated: true)
    }
}
