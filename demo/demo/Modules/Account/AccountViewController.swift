//
//  AccountViewController.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import UIKit
import Combine

class AccountViewController: ViewController, UITextFieldDelegate, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    private lazy var loader = UIActivityIndicatorView.makeForAutolayout()
        .set(\.hidesWhenStopped, to: true)
    private lazy var stackView = UIStackView.makeForAutolayout()
        .set(\.axis, to: .vertical)
        .set(\.alignment, to: .fill)
        .set(\.distribution, to: .equalSpacing)
        .set(\.spacing, to: 20)
    private lazy var avatarStackView = UIStackView.makeForAutolayout()
        .set(\.alignment, to: .center)
        .set(\.spacing, to: 20)
    private lazy var infoStackView = UIStackView.makeForAutolayout()
        .set(\.axis, to: .vertical)
        .set(\.spacing, to: 20)
    private lazy var pictureImageView = AvatarImageView.makeForAutolayout()
        .set(\.accessibilityIdentifier, to: "avatar_image_view")
    private lazy var firstNameTextField = TextField.makeForAutolayout()
        .set(\.validator, to: Validators.textNotEmpty)
        .set(\.returnKeyType, to: .next)
        .set(\.delegate, to: self)
        .set(\.placeholder, to: "First name")
        .set(\.accessibilityIdentifier, to: "first_name_field")
    private lazy var lastNameTextField = TextField.makeForAutolayout()
        .set(\.validator, to: Validators.textNotEmpty)
        .set(\.returnKeyType, to: .next)
        .set(\.delegate, to: self)
        .set(\.placeholder, to: "Second name")
        .set(\.accessibilityIdentifier, to: "second_name_field")
    private lazy var emailTextField = TextField.makeForAutolayout()
        .set(\.validator, to: Validators.email)
        .set(\.returnKeyType, to: .next)
        .set(\.delegate, to: self)
        .set(\.placeholder, to: "Email address")
        .set(\.accessibilityIdentifier, to: "email_field")
    private lazy var phoneTextField = TextField.makeForAutolayout()
        .set(\.validator, to: Validators.phoneNumber)
        .set(\.returnKeyType, to: .next)
        .set(\.delegate, to: self)
        .set(\.placeholder, to: "Phone number")
        .set(\.accessibilityIdentifier, to: "phone_field")
    private lazy var locationTextField = TextField.makeForAutolayout()
        .set(\.validator, to: Validators.textNotEmpty)
        .set(\.returnKeyType, to: .next)
        .set(\.delegate, to: self)
        .set(\.placeholder, to: "City")
        .set(\.accessibilityIdentifier, to: "location_field")
    
    private lazy var saveButton = UIButton()
        .set(\.title, to: "Save")
        .set(\.accessibilityIdentifier, to: "save_button")
        .set(\.titleColor, to: .blue)
    
    private lazy var logoutButton = UIButton()
        .set(\.title, to: "Logout")
        .set(\.accessibilityIdentifier, to: "logout_button")
        .set(\.titleColor, to: .blue)
    
    private lazy var pickerController = UIImagePickerController()
        .set(\.delegate, to: self)
        .set(\.allowsEditing, to: true)
        .set(\.mediaTypes, to: ["public.image"])
    private var allRequiredInputs: [InputField] { [firstNameTextField, lastNameTextField,
                                                   emailTextField, phoneTextField, locationTextField, pictureImageView] }
    private var cancellables = Set<AnyCancellable>()
    
    // MARK: - Lifecycyle
    
    override func viewDidLoad() {
        super.viewDidLoad()
        title = "Your account"
        initializeButtons()
    }
    
    override func initializeSubviews() {
        super.initializeSubviews()
        pictureImageView.backgroundColor = .darkGray
        view.addSubview(stackView)
        view.addSubview(loader)
        [avatarStackView, emailTextField, phoneTextField, locationTextField]
            .forEach(stackView.addArrangedSubview)
        [firstNameTextField, lastNameTextField].forEach(infoStackView.addArrangedSubview)
        [pictureImageView, infoStackView].forEach(avatarStackView.addArrangedSubview)
        navigationItem.rightBarButtonItem = UIBarButtonItem(customView: saveButton)
        navigationItem.leftBarButtonItem = UIBarButtonItem(customView: logoutButton)
        createConstraints()
    }
    
    override func createConstraints() {
        super.createConstraints()
        let layoutGuide = view.safeAreaLayoutGuide
        NSLayoutConstraint.activate([
            loader.centerYAnchor.constraint(equalTo: layoutGuide.centerYAnchor),
            loader.centerXAnchor.constraint(equalTo: layoutGuide.centerXAnchor),
            stackView.topAnchor.constraint(equalTo: layoutGuide.topAnchor, constant: 20),
            stackView.leadingAnchor.constraint(equalTo: layoutGuide.leadingAnchor, constant: 20),
            stackView.trailingAnchor.constraint(equalTo: layoutGuide.trailingAnchor, constant: -20),
            stackView.bottomAnchor.constraint(lessThanOrEqualTo: layoutGuide.bottomAnchor),
            pictureImageView.widthAnchor.constraint(equalToConstant: 125),
            pictureImageView.heightAnchor.constraint(equalToConstant: 125)
        ])
    }
    
    private func initializeButtons() {
        logoutButton.addTarget(self, action: #selector(onLogutTouched(_:)), for: .touchUpInside)
        saveButton.addTarget(self, action: #selector(onSaveTouched(_:)), for: .touchUpInside)
        pictureImageView.chooseImageButton.addTarget(self, action: #selector(onChangePictureTouched(_:)), for: .touchUpInside)
    }
    
    // MARK: - Actions
    
    @objc private func onSaveTouched(_ sender: Any) {
        view.endEditing(true)
        if allRequiredInputs.filter({ $0.forceValidation() }).count == allRequiredInputs.count {
            showAlert(with: "Success", message: "Data saved!")
        } else {
            // This code is not so great, but my time has done
            showAlert(with: "Ops...", message: "Please fullfill all required fields")
        }
    }
    
    
    @objc private func onChangePictureTouched(_ sender: Any) {
        let alertController = UIAlertController(title: "Update profile picture", message: "Choose source", preferredStyle: .actionSheet)
        if let action = self.action(for: .camera, title: "Take photo") {
            alertController.addAction(action)
        }
        if let action = self.action(for: .savedPhotosAlbum, title: "Camera roll") {
            alertController.addAction(action)
        }
        if let action = self.action(for: .photoLibrary, title: "Photo library") {
            alertController.addAction(action)
        }
        
        alertController.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))
        
        present(alertController, animated: true, completion: nil)
    }
    
    @objc private func onLogutTouched(_ sender: Any?) {
        let vc = ModuleFactory().makeLoginVC()
        navigationController?.setViewControllers([vc], animated: true)
    }
    
    // MARK: - ImagePicker
    
    private func showImagePicker(type: UIImagePickerController.SourceType) {
        pickerController.sourceType = type
        present(pickerController, animated: true, completion: nil)
    }
    
    private func action(for type: UIImagePickerController.SourceType, title: String) -> UIAlertAction? {
        guard UIImagePickerController.isSourceTypeAvailable(type) else {
            return nil
        }
        
        return UIAlertAction(title: title, style: .default, handler: { [weak self] _ in
            self?.showImagePicker(type: type)
        })
    }
    
    // MARK: - UIImagePickerControllerDelegate, UINavigationControllerDelegate
    
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        picker.dismiss(animated: true, completion: nil)
    }
    
    func imagePickerController(_ picker: UIImagePickerController,
                               didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey: Any]) {
        defer { picker.dismiss(animated: true, completion: nil) }
        guard let image = info[.editedImage] as? UIImage else {
            return
        }
        pictureImageView.image = image
    }
    
    // MARK: - UITextFieldDelegate
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        switch textField {
        case firstNameTextField:
            lastNameTextField.becomeFirstResponder()
        case lastNameTextField:
            emailTextField.becomeFirstResponder()
        case emailTextField:
            phoneTextField.becomeFirstResponder()
        case phoneTextField:
            locationTextField.becomeFirstResponder()
        default: break
        }
        return true
    }
}
